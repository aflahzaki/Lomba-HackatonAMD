"""Tests for FastAPI endpoints."""

import os
import sys
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
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


class TestHealthEndpoint:
    """Test GET /api/health."""

    def test_health_returns_200(self, client):
        """Health endpoint should return 200."""
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_response_fields(self, client):
        """Health response should contain expected fields."""
        response = client.get("/api/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "model_loaded" in data
        assert "sidata_loaded" in data
        assert "sidata_programs" in data
        assert data["sidata_programs"] > 3000


class TestPredictEndpoint:
    """Test POST /api/predict."""

    def test_predict_valid_payload(self, client):
        """Should return probability for valid input."""
        payload = {
            "scores": {
                "Matematika": {"sem1": 85, "sem2": 87, "sem3": 88, "sem4": 90, "sem5": 92},
                "Fisika": {"sem1": 80, "sem2": 82, "sem3": 84, "sem4": 86, "sem5": 88},
            },
            "school_ranking": 5,
            "total_students": 200,
            "school_accreditation": "A",
            "target_program_id": "TEKNIK SIPIL",
        }
        response = client.post("/api/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert 0 <= data["probability"] <= 100
        assert "confidence_lower" in data
        assert "confidence_upper" in data
        assert data["confidence_lower"] < data["confidence_upper"]
        assert len(data["variables"]) == 6

    def test_predict_with_program_code(self, client):
        """Should work with kode_prodi as target."""
        payload = {
            "scores": {
                "Matematika": {"sem1": 80, "sem2": 82},
            },
            "school_ranking": 10,
            "total_students": 100,
            "school_accreditation": "B",
            "target_program_id": "111001",
        }
        response = client.post("/api/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert 0 <= data["probability"] <= 100

    def test_predict_has_input_summary(self, client):
        """Response should include input summary."""
        payload = {
            "scores": {"Math": {"s1": 85}},
            "school_ranking": 3,
            "total_students": 50,
            "school_accreditation": "A",
            "target_program_id": "TEKNIK MESIN",
            "jurusan": "IPA",
        }
        response = client.post("/api/predict", json=payload)
        data = response.json()
        assert "input_summary" in data
        assert "avg_score" in data["input_summary"]
        assert "ranking" in data["input_summary"]

    def test_predict_has_recommendations(self, client):
        """Response should include recommendations list."""
        payload = {
            "scores": {"Math": {"s1": 80}},
            "school_ranking": 10,
            "total_students": 100,
            "school_accreditation": "B",
            "target_program_id": "TEKNIK SIPIL",
        }
        response = client.post("/api/predict", json=payload)
        data = response.json()
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)

    def test_predict_unknown_program(self, client):
        """Should still work with unknown program (uses defaults)."""
        payload = {
            "scores": {"Math": {"s1": 75}},
            "school_ranking": 20,
            "total_students": 100,
            "school_accreditation": "C",
            "target_program_id": "PROGRAM_TIDAK_ADA_XYZ",
        }
        response = client.post("/api/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert 0 <= data["probability"] <= 100

    def test_predict_missing_field(self, client):
        """Should return 422 for missing required field."""
        payload = {
            "scores": {"Math": {"s1": 80}},
            # Missing school_ranking
            "total_students": 100,
            "school_accreditation": "A",
            "target_program_id": "TEKNIK SIPIL",
        }
        response = client.post("/api/predict", json=payload)
        assert response.status_code == 422

    def test_predict_invalid_score_value(self, client):
        """Should return 422 for non-numeric score values."""
        payload = {
            "scores": {"Math": {"s1": "abc"}},
            "school_ranking": 10,
            "total_students": 100,
            "school_accreditation": "B",
            "target_program_id": "TEKNIK SIPIL",
        }
        response = client.post("/api/predict", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert "Invalid score value" in data["detail"]


class TestRecommendEndpoint:
    """Test POST /api/recommend."""

    def test_recommend_valid_payload(self, client):
        """Should return recommendations for valid input."""
        payload = {
            "scores": {"Math": {"s1": 80, "s2": 82}},
            "school_ranking": 10,
            "total_students": 100,
            "school_accreditation": "B",
            "target_program_id": "TEKNIK SIPIL",
        }
        response = client.post("/api/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "target_program" in data
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)

    def test_recommend_returns_list(self, client):
        """Recommendations should be a list of programs."""
        payload = {
            "scores": {"Math": {"s1": 80}},
            "school_ranking": 5,
            "total_students": 100,
            "school_accreditation": "A",
            "target_program_id": "TEKNIK SIPIL",
            "limit": 3,
        }
        response = client.post("/api/recommend", json=payload)
        data = response.json()
        for rec in data["recommendations"]:
            assert "name" in rec
            assert "university" in rec
            assert "ratio" in rec
            assert "daya_tampung" in rec
            assert "comparison" in rec

    def test_recommend_unknown_program(self, client):
        """Should return empty recommendations for unknown program."""
        payload = {
            "scores": {"Math": {"s1": 80}},
            "school_ranking": 10,
            "total_students": 100,
            "school_accreditation": "B",
            "target_program_id": "PROGRAM_TIDAK_ADA_XYZ",
        }
        response = client.post("/api/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["recommendations"] == []


class TestAdvisorEndpoint:
    """Test POST /api/advisor."""

    def test_advisor_returns_reply(self, client):
        """Should return a reply (fallback when no API key)."""
        payload = {
            "message": "Bagaimana cara meningkatkan peluang SNBP saya?",
            "context": {
                "probability": 45.5,
                "variables": [
                    {"name": "Rasio Kompetisi", "normalized_score": 0.5, "weight": 0.30}
                ],
                "input_summary": {
                    "avg_score": 82.0,
                    "target_program": "TEKNIK INFORMATIKA",
                },
            },
        }
        response = client.post("/api/advisor", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
        assert len(data["reply"]) > 0
        assert "suggestions" in data
        assert isinstance(data["suggestions"], list)

    def test_advisor_without_context(self, client):
        """Should work without prediction context."""
        payload = {
            "message": "Apa itu SNBP?",
        }
        response = client.post("/api/advisor", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
        assert len(data["reply"]) > 0

    def test_advisor_empty_message(self, client):
        """Should reject empty message."""
        payload = {
            "message": "",
        }
        response = client.post("/api/advisor", json=payload)
        assert response.status_code == 400

    @patch("app.services.advisor.settings")
    def test_advisor_with_mock_fireworks(self, mock_settings, client):
        """Should use fallback when API key is empty."""
        mock_settings.FIREWORKS_API_KEY = ""
        payload = {
            "message": "Berapa peluang saya?",
            "context": {"probability": 70},
        }
        response = client.post("/api/advisor", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
