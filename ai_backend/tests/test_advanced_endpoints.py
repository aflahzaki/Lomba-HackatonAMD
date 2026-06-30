"""Tests for advanced AI/ML endpoints: explain, batch predict, what-if."""

import os
import sys
from unittest.mock import patch

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


@pytest.fixture
def valid_payload():
    """Standard valid payload for testing."""
    return {
        "scores": {
            "Matematika": {"sem1": 85, "sem2": 87, "sem3": 88, "sem4": 90, "sem5": 92},
            "Fisika": {"sem1": 80, "sem2": 82, "sem3": 84, "sem4": 86, "sem5": 88},
        },
        "school_ranking": 5,
        "total_students": 200,
        "school_accreditation": "A",
        "target_program_id": "TEKNIK SIPIL",
    }


class TestExplainEndpoint:
    """Test POST /api/explain."""

    def test_explain_returns_200(self, client, valid_payload):
        """Should return 200 with valid input."""
        response = client.post("/api/explain", json=valid_payload)
        assert response.status_code == 200

    def test_explain_response_structure(self, client, valid_payload):
        """Should return complete ExplainResponse with all fields."""
        response = client.post("/api/explain", json=valid_payload)
        data = response.json()
        assert data["success"] is True
        assert "shap_values" in data
        assert "base_value" in data
        assert "prediction" in data
        assert "explanation_text" in data

    def test_explain_shap_values_structure(self, client, valid_payload):
        """Each SHAP value should have feature, value, contribution, description."""
        response = client.post("/api/explain", json=valid_payload)
        data = response.json()
        assert len(data["shap_values"]) == 6
        for sv in data["shap_values"]:
            assert "feature" in sv
            assert "value" in sv
            assert "contribution" in sv
            assert "description" in sv
            assert isinstance(sv["contribution"], (int, float))

    def test_explain_shap_values_sorted_by_impact(self, client, valid_payload):
        """SHAP values should be sorted by absolute contribution descending."""
        response = client.post("/api/explain", json=valid_payload)
        data = response.json()
        contributions = [abs(sv["contribution"]) for sv in data["shap_values"]]
        assert contributions == sorted(contributions, reverse=True)

    def test_explain_prediction_in_range(self, client, valid_payload):
        """Prediction should be between 0 and 1."""
        response = client.post("/api/explain", json=valid_payload)
        data = response.json()
        assert 0 <= data["prediction"] <= 1

    def test_explain_explanation_text_in_indonesian(self, client, valid_payload):
        """Explanation text should be in Indonesian."""
        response = client.post("/api/explain", json=valid_payload)
        data = response.json()
        assert len(data["explanation_text"]) > 0
        # Check for Indonesian keywords
        text = data["explanation_text"].lower()
        assert any(word in text for word in ["faktor", "peluang", "tidak ada"])

    def test_explain_unknown_program(self, client):
        """Should work with unknown program (uses defaults)."""
        payload = {
            "scores": {"Math": {"s1": 75}},
            "school_ranking": 20,
            "total_students": 100,
            "school_accreditation": "C",
            "target_program_id": "PROGRAM_TIDAK_ADA_XYZ",
        }
        response = client.post("/api/explain", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["shap_values"]) == 6

    def test_explain_missing_field(self, client):
        """Should return 422 for missing required field."""
        payload = {
            "scores": {"Math": {"s1": 80}},
            # Missing school_ranking
            "total_students": 100,
            "school_accreditation": "A",
            "target_program_id": "TEKNIK SIPIL",
        }
        response = client.post("/api/explain", json=payload)
        assert response.status_code == 422

    def test_explain_invalid_scores(self, client):
        """Should return 422 for non-numeric score values."""
        payload = {
            "scores": {"Math": {"s1": "abc"}},
            "school_ranking": 10,
            "total_students": 100,
            "school_accreditation": "B",
            "target_program_id": "TEKNIK SIPIL",
        }
        response = client.post("/api/explain", json=payload)
        assert response.status_code == 422

    def test_explain_fallback_when_shap_fails(self, client, valid_payload):
        """Should still return results when SHAP computation fails (uses fallback)."""
        with patch("app.services.explainer.compute_shap_values") as mock_shap:
            # Simulate fallback by returning deterministic values
            mock_shap.side_effect = lambda features: (
                [0.1, -0.05, 0.02, -0.15, 0.01, 0.03],
                0.5,
            )
            response = client.post("/api/explain", json=valid_payload)
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert len(data["shap_values"]) == 6


class TestBatchPredictEndpoint:
    """Test POST /api/predict/batch."""

    def test_batch_single_student(self, client, valid_payload):
        """Should work with a single student."""
        response = client.post("/api/predict/batch", json={"students": [valid_payload]})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["results"]) == 1
        assert "summary" in data

    def test_batch_multiple_students(self, client):
        """Should work with multiple students."""
        students = [
            {
                "scores": {"Math": {"s1": 85, "s2": 87}},
                "school_ranking": 5,
                "total_students": 200,
                "school_accreditation": "A",
                "target_program_id": "TEKNIK SIPIL",
            },
            {
                "scores": {"Math": {"s1": 75, "s2": 78}},
                "school_ranking": 30,
                "total_students": 200,
                "school_accreditation": "B",
                "target_program_id": "TEKNIK MESIN",
            },
            {
                "scores": {"Math": {"s1": 90, "s2": 92}},
                "school_ranking": 2,
                "total_students": 150,
                "school_accreditation": "A",
                "target_program_id": "TEKNIK INFORMATIKA",
            },
        ]
        response = client.post("/api/predict/batch", json={"students": students})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["results"]) == 3

    def test_batch_summary_stats(self, client):
        """Should return correct summary statistics."""
        students = [
            {
                "scores": {"Math": {"s1": 85}},
                "school_ranking": 5,
                "total_students": 200,
                "school_accreditation": "A",
                "target_program_id": "TEKNIK SIPIL",
            },
            {
                "scores": {"Math": {"s1": 70}},
                "school_ranking": 50,
                "total_students": 200,
                "school_accreditation": "C",
                "target_program_id": "TEKNIK SIPIL",
            },
        ]
        response = client.post("/api/predict/batch", json={"students": students})
        data = response.json()
        summary = data["summary"]
        assert summary["count"] == 2
        assert "avg_probability" in summary
        assert "highest" in summary
        assert "lowest" in summary
        assert summary["highest"] >= summary["lowest"]
        assert summary["lowest"] <= summary["avg_probability"] <= summary["highest"]

    def test_batch_over_50_students_rejected(self, client, valid_payload):
        """Should return 422 if more than 50 students submitted."""
        students = [valid_payload] * 51
        response = client.post("/api/predict/batch", json={"students": students})
        assert response.status_code == 422

    def test_batch_empty_students_rejected(self, client):
        """Should return 422 if no students submitted."""
        response = client.post("/api/predict/batch", json={"students": []})
        assert response.status_code == 422

    def test_batch_exactly_50_students_accepted(self, client, valid_payload):
        """Should accept exactly 50 students."""
        students = [valid_payload] * 50
        response = client.post("/api/predict/batch", json={"students": students})
        assert response.status_code == 200
        data = response.json()
        assert data["summary"]["count"] == 50

    def test_batch_individual_results_structure(self, client, valid_payload):
        """Each individual result should match PredictionResponse structure."""
        response = client.post("/api/predict/batch", json={"students": [valid_payload]})
        data = response.json()
        result = data["results"][0]
        assert result["success"] is True
        assert 0 <= result["probability"] <= 100
        assert "confidence_lower" in result
        assert "confidence_upper" in result
        assert "variables" in result
        assert len(result["variables"]) == 6
        assert "input_summary" in result
        assert "timestamp" in result

    def test_batch_invalid_student_data(self, client):
        """Should return 422 for invalid student data in batch."""
        students = [
            {
                "scores": {"Math": {"s1": "invalid"}},
                "school_ranking": 5,
                "total_students": 200,
                "school_accreditation": "A",
                "target_program_id": "TEKNIK SIPIL",
            },
        ]
        response = client.post("/api/predict/batch", json={"students": students})
        assert response.status_code == 422


class TestWhatIfEndpoint:
    """Test POST /api/what-if."""

    def test_what_if_change_avg_score(self, client, valid_payload):
        """Should compute what-if for changing avg_score."""
        payload = {
            **valid_payload,
            "variable_to_change": "avg_score",
            "new_value": "95",
        }
        response = client.post("/api/what-if", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "original_probability" in data
        assert "new_probability" in data
        assert "change" in data
        assert data["variable_changed"] == "avg_score"
        assert "insight" in data

    def test_what_if_change_school_ranking(self, client, valid_payload):
        """Should compute what-if for changing school_ranking."""
        payload = {
            **valid_payload,
            "variable_to_change": "school_ranking",
            "new_value": "1",
        }
        response = client.post("/api/what-if", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["variable_changed"] == "school_ranking"

    def test_what_if_change_accreditation(self, client, valid_payload):
        """Should compute what-if for changing school_accreditation."""
        payload = {
            **valid_payload,
            "school_accreditation": "C",
            "variable_to_change": "school_accreditation",
            "new_value": "A",
        }
        response = client.post("/api/what-if", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["variable_changed"] == "school_accreditation"

    def test_what_if_change_program(self, client, valid_payload):
        """Should compute what-if for changing target_program_id."""
        payload = {
            **valid_payload,
            "variable_to_change": "target_program_id",
            "new_value": "TEKNIK MESIN",
        }
        response = client.post("/api/what-if", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["variable_changed"] == "target_program_id"

    def test_what_if_change_delta_computed_correctly(self, client, valid_payload):
        """Change should equal new_probability - original_probability."""
        payload = {
            **valid_payload,
            "variable_to_change": "avg_score",
            "new_value": "95",
        }
        response = client.post("/api/what-if", json=payload)
        data = response.json()
        expected_change = round(data["new_probability"] - data["original_probability"], 1)
        assert abs(data["change"] - expected_change) < 0.2  # Allow small rounding tolerance

    def test_what_if_insight_in_indonesian(self, client, valid_payload):
        """Insight message should be in Indonesian."""
        payload = {
            **valid_payload,
            "variable_to_change": "avg_score",
            "new_value": "95",
        }
        response = client.post("/api/what-if", json=payload)
        data = response.json()
        assert len(data["insight"]) > 0
        # Check for Indonesian keywords
        text = data["insight"].lower()
        assert any(word in text for word in ["mengubah", "peluang", "perubahan"])

    def test_what_if_invalid_variable(self, client, valid_payload):
        """Should return 422 for invalid variable_to_change."""
        payload = {
            **valid_payload,
            "variable_to_change": "invalid_variable",
            "new_value": "95",
        }
        response = client.post("/api/what-if", json=payload)
        assert response.status_code == 422

    def test_what_if_invalid_avg_score_value(self, client, valid_payload):
        """Should return 422 for non-numeric avg_score value."""
        payload = {
            **valid_payload,
            "variable_to_change": "avg_score",
            "new_value": "not_a_number",
        }
        response = client.post("/api/what-if", json=payload)
        assert response.status_code == 422

    def test_what_if_invalid_ranking_value(self, client, valid_payload):
        """Should return 422 for non-numeric school_ranking value."""
        payload = {
            **valid_payload,
            "variable_to_change": "school_ranking",
            "new_value": "abc",
        }
        response = client.post("/api/what-if", json=payload)
        assert response.status_code == 422

    def test_what_if_invalid_accreditation_value(self, client, valid_payload):
        """Should return 422 for invalid accreditation value."""
        payload = {
            **valid_payload,
            "variable_to_change": "school_accreditation",
            "new_value": "X",
        }
        response = client.post("/api/what-if", json=payload)
        assert response.status_code == 422

    def test_what_if_probabilities_in_range(self, client, valid_payload):
        """Both original and new probability should be between 0 and 100."""
        payload = {
            **valid_payload,
            "variable_to_change": "avg_score",
            "new_value": "95",
        }
        response = client.post("/api/what-if", json=payload)
        data = response.json()
        assert 0 <= data["original_probability"] <= 100
        assert 0 <= data["new_probability"] <= 100

    def test_what_if_missing_required_field(self, client):
        """Should return 422 if variable_to_change or new_value missing."""
        payload = {
            "scores": {"Math": {"s1": 85}},
            "school_ranking": 5,
            "total_students": 200,
            "school_accreditation": "A",
            "target_program_id": "TEKNIK SIPIL",
            # Missing variable_to_change and new_value
        }
        response = client.post("/api/what-if", json=payload)
        assert response.status_code == 422


class TestExplainerService:
    """Test the explainer service directly."""

    def test_explain_prediction_returns_dict(self):
        """explain_prediction should return a properly structured dict."""
        from app.services.explainer import explain_prediction

        result = explain_prediction(
            avg_score=85.0,
            ranking_percentile=0.05,
            accreditation="A",
            program=None,
        )
        assert "shap_values" in result
        assert "base_value" in result
        assert "prediction" in result
        assert "explanation_text" in result

    def test_explain_prediction_six_features(self):
        """Should return exactly 6 feature contributions."""
        from app.services.explainer import explain_prediction

        result = explain_prediction(
            avg_score=85.0,
            ranking_percentile=0.05,
            accreditation="A",
            program=None,
        )
        assert len(result["shap_values"]) == 6

    def test_fallback_importance_works(self):
        """Fallback importance should work when model has no SHAP support."""
        import numpy as np
        from app.services.explainer import _fallback_importance

        features = np.array([[85.0, 0.05, 1.0, 5.0, 0.1, 100.0]])
        shap_vals, base_value = _fallback_importance(features)
        assert len(shap_vals) == 6
        assert isinstance(base_value, float)

    def test_compute_shap_values_returns_tuple(self):
        """compute_shap_values should return (list, float) tuple."""
        import numpy as np
        from app.services.explainer import compute_shap_values

        features = np.array([[85.0, 0.05, 1.0, 5.0, 0.1, 100.0]])
        shap_vals, base_value = compute_shap_values(features)
        assert isinstance(shap_vals, list)
        assert len(shap_vals) == 6
        assert isinstance(base_value, float)


class TestMetricsAdvancedTracking:
    """Test that metrics track the new endpoints."""

    def test_metrics_include_explanations_count(self, client, valid_payload):
        """Metrics should track total_explanations."""
        response = client.get("/api/metrics")
        data = response.json()
        assert "total_explanations" in data

    def test_metrics_include_batch_count(self, client, valid_payload):
        """Metrics should track total_batch_requests."""
        response = client.get("/api/metrics")
        data = response.json()
        assert "total_batch_requests" in data

    def test_metrics_include_what_if_count(self, client, valid_payload):
        """Metrics should track total_what_if."""
        response = client.get("/api/metrics")
        data = response.json()
        assert "total_what_if" in data
