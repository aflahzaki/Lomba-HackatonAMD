"""Tests for production middleware: security headers, metrics, error handling, rate limiting."""

import os
import sys
import time

import pytest
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.middleware.metrics import metrics
from app.models.predictor import predictor


@pytest.fixture(scope="module", autouse=True)
def setup_predictor():
    """Load SIDATA and model before tests."""
    sql_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "database",
        "seed_sidata.sql",
    )
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "models",
        "prediction_model.joblib",
    )
    predictor.load_sidata(sql_path)
    predictor.load_model(model_path)


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestSecurityHeaders:
    """Test security headers middleware."""

    def test_health_has_x_content_type_options(self, client):
        """Every response should have X-Content-Type-Options header."""
        response = client.get("/api/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"

    def test_health_has_x_frame_options(self, client):
        """Every response should have X-Frame-Options header."""
        response = client.get("/api/health")
        assert response.headers.get("X-Frame-Options") == "DENY"

    def test_health_has_x_xss_protection(self, client):
        """Every response should have X-XSS-Protection header."""
        response = client.get("/api/health")
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"

    def test_health_has_content_security_policy(self, client):
        """Every response should have Content-Security-Policy header."""
        response = client.get("/api/health")
        assert response.headers.get("Content-Security-Policy") == "default-src 'self'"

    def test_predict_has_security_headers(self, client):
        """POST endpoints should also have security headers."""
        payload = {
            "scores": {"Math": {"s1": 85}},
            "school_ranking": 5,
            "total_students": 100,
            "school_accreditation": "A",
            "target_program_id": "TEKNIK SIPIL",
        }
        response = client.post("/api/predict", json=payload)
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert response.headers.get("Content-Security-Policy") == "default-src 'self'"

    def test_metrics_has_security_headers(self, client):
        """Metrics endpoint should also have security headers."""
        response = client.get("/api/metrics")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"


class TestMetricsEndpoint:
    """Test GET /api/metrics endpoint."""

    def test_metrics_returns_200(self, client):
        """Metrics endpoint should return 200."""
        response = client.get("/api/metrics")
        assert response.status_code == 200

    def test_metrics_has_total_predictions(self, client):
        """Metrics should include total_predictions field."""
        response = client.get("/api/metrics")
        data = response.json()
        assert "total_predictions" in data
        assert isinstance(data["total_predictions"], int)

    def test_metrics_has_avg_response_time(self, client):
        """Metrics should include avg_response_time_ms field."""
        response = client.get("/api/metrics")
        data = response.json()
        assert "avg_response_time_ms" in data
        assert isinstance(data["avg_response_time_ms"], (int, float))

    def test_metrics_has_model_version(self, client):
        """Metrics should include model_version field."""
        response = client.get("/api/metrics")
        data = response.json()
        assert "model_version" in data
        assert isinstance(data["model_version"], str)

    def test_metrics_has_uptime_seconds(self, client):
        """Metrics should include uptime_seconds field."""
        response = client.get("/api/metrics")
        data = response.json()
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], (int, float))
        assert data["uptime_seconds"] >= 0

    def test_metrics_has_total_requests(self, client):
        """Metrics should include total_requests field."""
        response = client.get("/api/metrics")
        data = response.json()
        assert "total_requests" in data
        assert isinstance(data["total_requests"], int)

    def test_metrics_has_popular_programs(self, client):
        """Metrics should include popular_programs field."""
        response = client.get("/api/metrics")
        data = response.json()
        assert "popular_programs" in data
        assert isinstance(data["popular_programs"], list)

    def test_metrics_has_endpoint_stats(self, client):
        """Metrics should include endpoint_stats field."""
        response = client.get("/api/metrics")
        data = response.json()
        assert "endpoint_stats" in data
        assert isinstance(data["endpoint_stats"], dict)


class TestGlobalExceptionHandler:
    """Test global exception handler."""

    def test_unhandled_exception_returns_500_json(self, client):
        """Unhandled exceptions should return consistent JSON error format."""
        from unittest.mock import patch

        # Patch predictor.sidata.find_program to raise an unexpected error
        with patch.object(
            predictor.sidata, "find_program", side_effect=RuntimeError("Unexpected DB error")
        ):
            payload = {
                "scores": {"Math": {"s1": 85}},
                "school_ranking": 5,
                "total_students": 100,
                "school_accreditation": "A",
                "target_program_id": "TEKNIK SIPIL",
            }
            response = client.post("/api/predict", json=payload)
            assert response.status_code == 500
            data = response.json()
            assert data["success"] is False
            assert "error" in data
            assert "detail" in data
            assert "timestamp" in data
            assert data["error"] == "RuntimeError"

    def test_exception_handler_has_timestamp(self, client):
        """Error response should include an ISO timestamp."""
        from unittest.mock import patch

        with patch.object(
            predictor.sidata, "find_program", side_effect=ValueError("test error")
        ):
            payload = {
                "scores": {"Math": {"s1": 85}},
                "school_ranking": 5,
                "total_students": 100,
                "school_accreditation": "A",
                "target_program_id": "TEKNIK SIPIL",
            }
            response = client.post("/api/predict", json=payload)
            assert response.status_code == 500
            data = response.json()
            assert "timestamp" in data
            # Should be a valid ISO datetime string
            assert "T" in data["timestamp"]


class TestMetricsCollector:
    """Test the MetricsCollector class directly."""

    def test_record_request(self):
        """Should increment request counter and record time."""
        from app.middleware.metrics import MetricsCollector

        m = MetricsCollector()
        m.record_request("/api/health", 10.5)
        assert m.total_requests == 1
        assert m.total_response_time_ms == 10.5
        assert m.endpoint_stats["/api/health"] == 1

    def test_record_prediction(self):
        """Should increment prediction counter and track program."""
        from app.middleware.metrics import MetricsCollector

        m = MetricsCollector()
        m.record_prediction("TEKNIK INFORMATIKA")
        assert m.total_predictions == 1
        assert m.program_requests["TEKNIK INFORMATIKA"] == 1

    def test_avg_response_time_calculation(self):
        """Should calculate average response time correctly."""
        from app.middleware.metrics import MetricsCollector

        m = MetricsCollector()
        m.record_request("/api/health", 10.0)
        m.record_request("/api/predict", 30.0)
        assert m.avg_response_time_ms == 20.0

    def test_avg_response_time_zero_requests(self):
        """Should return 0 when no requests have been made."""
        from app.middleware.metrics import MetricsCollector

        m = MetricsCollector()
        assert m.avg_response_time_ms == 0.0

    def test_popular_programs_top_5(self):
        """Should return top 5 programs by request count."""
        from app.middleware.metrics import MetricsCollector

        m = MetricsCollector()
        for i in range(10):
            m.record_prediction("Program A")
        for i in range(8):
            m.record_prediction("Program B")
        for i in range(6):
            m.record_prediction("Program C")
        for i in range(4):
            m.record_prediction("Program D")
        for i in range(2):
            m.record_prediction("Program E")
        for i in range(1):
            m.record_prediction("Program F")

        popular = m.popular_programs
        assert len(popular) == 5
        assert popular[0]["program"] == "Program A"
        assert popular[0]["count"] == 10

    def test_uptime_seconds(self):
        """Should report positive uptime."""
        from app.middleware.metrics import MetricsCollector

        m = MetricsCollector()
        time.sleep(0.01)
        assert m.uptime_seconds > 0

    def test_get_metrics_returns_dict(self):
        """get_metrics should return a complete metrics dictionary."""
        from app.middleware.metrics import MetricsCollector

        m = MetricsCollector()
        result = m.get_metrics()
        assert "total_predictions" in result
        assert "total_requests" in result
        assert "avg_response_time_ms" in result
        assert "model_version" in result
        assert "uptime_seconds" in result
        assert "popular_programs" in result
        assert "endpoint_stats" in result


class TestRateLimiting:
    """Test rate limiting configuration."""

    def test_rate_limit_handler_returns_429(self):
        """Rate limit handler should return 429 with JSON error body."""
        import json
        from unittest.mock import MagicMock

        from slowapi.errors import RateLimitExceeded

        from app.middleware.rate_limiter import rate_limit_exceeded_handler

        mock_request = MagicMock()
        # Create RateLimitExceeded manually since it requires a Limit object
        exc = RateLimitExceeded.__new__(RateLimitExceeded)
        exc.status_code = 429
        exc.detail = "10 per 1 minute"

        response = rate_limit_exceeded_handler(mock_request, exc)
        assert response.status_code == 429
        body = json.loads(response.body)
        assert body["success"] is False
        assert body["error"] == "Rate limit exceeded"
        assert "detail" in body

    def test_rate_limit_handler_json_structure(self):
        """Rate limit handler response should have success, error, detail fields."""
        import json
        from unittest.mock import MagicMock

        from slowapi.errors import RateLimitExceeded

        from app.middleware.rate_limiter import rate_limit_exceeded_handler

        mock_request = MagicMock()
        exc = RateLimitExceeded.__new__(RateLimitExceeded)
        exc.status_code = 429
        exc.detail = "30 per 1 minute"

        response = rate_limit_exceeded_handler(mock_request, exc)
        body = json.loads(response.body)
        assert body["success"] is False
        assert body["error"] == "Rate limit exceeded"
        assert body["detail"] == "30 per 1 minute"
