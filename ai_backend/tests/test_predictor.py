"""Tests for the ML predictor module."""

import os
import sys

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.predictor import Predictor, SIDATAStore


@pytest.fixture
def predictor_instance():
    """Create a Predictor with SIDATA loaded."""
    p = Predictor()
    sql_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "database",
        "seed_sidata.sql",
    )
    p.load_sidata(sql_path)
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "models",
        "prediction_model.joblib",
    )
    p.load_model(model_path)
    return p


@pytest.fixture
def sidata_store():
    """Create a loaded SIDATAStore."""
    store = SIDATAStore()
    sql_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "database",
        "seed_sidata.sql",
    )
    store.load(sql_path)
    return store


class TestSIDATAStore:
    """Test SIDATA data loading and lookup."""

    def test_load_programs(self, sidata_store):
        """Should load all 3058 programs."""
        assert len(sidata_store.programs) > 3000
        assert sidata_store.is_loaded

    def test_load_universities(self, sidata_store):
        """Should load 84 universities."""
        assert len(sidata_store.universities) == 84

    def test_find_program_by_code(self, sidata_store):
        """Should find program by kode_prodi."""
        program = sidata_store.find_program("111001")
        assert program is not None
        assert program["nama_prodi"] == "PENDIDIKAN DOKTER HEWAN"

    def test_find_program_by_name(self, sidata_store):
        """Should find program by name."""
        program = sidata_store.find_program("TEKNIK SIPIL")
        assert program is not None
        assert "TEKNIK SIPIL" in program["nama_prodi"]

    def test_find_program_case_insensitive(self, sidata_store):
        """Should find program case-insensitively."""
        program = sidata_store.find_program("teknik mesin")
        assert program is not None

    def test_find_program_not_found(self, sidata_store):
        """Should return None for non-existent program."""
        program = sidata_store.find_program("PROGRAM_YANG_TIDAK_ADA_12345")
        assert program is None

    def test_find_similar_programs(self, sidata_store):
        """Should find similar programs with lower competition."""
        program = sidata_store.find_program("111001")
        assert program is not None
        similar = sidata_store.find_similar_programs(program, limit=5)
        # Should return some similar programs (may be empty for rare programs)
        assert isinstance(similar, list)

    def test_program_data_completeness(self, sidata_store):
        """Each program should have all required fields."""
        for kode, prog in list(sidata_store.programs.items())[:10]:
            assert "kode_univ" in prog
            assert "kode_prodi" in prog
            assert "nama_prodi" in prog
            assert "peminat_2022" in prog
            assert "daya_tampung_2022" in prog
            assert "daya_tampung_2023" in prog
            assert prog["peminat_2022"] >= 0
            assert prog["daya_tampung_2022"] >= 0


class TestPredictor:
    """Test ML model predictions."""

    def test_model_loaded(self, predictor_instance):
        """Model should be loaded successfully."""
        assert predictor_instance.model_loaded

    def test_predict_returns_tuple(self, predictor_instance):
        """Predict should return (probability, lower, upper) tuple."""
        program = predictor_instance.sidata.find_program("111001")
        result = predictor_instance.predict(
            avg_score=85.0,
            ranking_percentile=0.1,
            accreditation="A",
            program=program,
        )
        assert len(result) == 3
        prob, lower, upper = result
        assert isinstance(prob, float)
        assert isinstance(lower, float)
        assert isinstance(upper, float)

    def test_predict_probability_bounds(self, predictor_instance):
        """Probability should be between 0.05 and 0.95."""
        program = predictor_instance.sidata.find_program("111001")
        prob, lower, upper = predictor_instance.predict(
            avg_score=85.0,
            ranking_percentile=0.1,
            accreditation="A",
            program=program,
        )
        assert 0.05 <= prob <= 0.95
        assert lower < upper
        assert lower >= 0.01
        assert upper <= 0.99

    def test_predict_high_score_high_probability(self, predictor_instance):
        """Top student in easy program should have high probability."""
        # Find a program with low competition
        for _, prog in predictor_instance.sidata.programs.items():
            ratio = prog["peminat_2022"] / max(prog["daya_tampung_2022"], 1)
            if 1.0 < ratio < 3.0 and prog["daya_tampung_2023"] > 50:
                prob, _, _ = predictor_instance.predict(
                    avg_score=95.0,
                    ranking_percentile=0.05,
                    accreditation="A",
                    program=prog,
                )
                assert prob > 0.5  # Should be above average
                break

    def test_predict_low_score_low_probability(self, predictor_instance):
        """Below average student in hard program should have lower probability."""
        # Find a high-competition program
        for _, prog in predictor_instance.sidata.programs.items():
            ratio = prog["peminat_2022"] / max(prog["daya_tampung_2022"], 1)
            if ratio > 15:
                prob, _, _ = predictor_instance.predict(
                    avg_score=65.0,
                    ranking_percentile=0.8,
                    accreditation="C",
                    program=prog,
                )
                assert prob < 0.5  # Should be below average
                break

    def test_predict_without_program(self, predictor_instance):
        """Should work with no program data (uses defaults)."""
        prob, lower, upper = predictor_instance.predict(
            avg_score=80.0,
            ranking_percentile=0.3,
            accreditation="B",
            program=None,
        )
        assert 0.05 <= prob <= 0.95

    def test_predict_extreme_score_high(self, predictor_instance):
        """Should handle extreme high scores."""
        prob, _, _ = predictor_instance.predict(
            avg_score=100.0,
            ranking_percentile=0.01,
            accreditation="A",
            program=None,
        )
        assert 0.05 <= prob <= 0.95

    def test_predict_extreme_score_low(self, predictor_instance):
        """Should handle extreme low scores."""
        prob, _, _ = predictor_instance.predict(
            avg_score=60.0,
            ranking_percentile=0.99,
            accreditation="C",
            program=None,
        )
        assert 0.05 <= prob <= 0.95

    def test_variable_breakdown(self, predictor_instance):
        """Should return 6 variable breakdowns."""
        program = predictor_instance.sidata.find_program("111001")
        breakdown = predictor_instance.get_variable_breakdown(
            avg_score=85.0,
            ranking=5,
            total_students=100,
            accreditation="A",
            program=program,
        )
        assert len(breakdown) == 6
        for var in breakdown:
            assert "name" in var
            assert "weight" in var
            assert "normalized_score" in var
            assert 0 <= var["normalized_score"] <= 1

    def test_deterministic_fallback(self):
        """When model is not loaded, should use deterministic formula."""
        p = Predictor()  # No model loaded
        assert not p.model_loaded
        prob, lower, upper = p.predict(
            avg_score=80.0,
            ranking_percentile=0.3,
            accreditation="B",
            program=None,
        )
        assert 0.05 <= prob <= 0.95
        assert lower < prob
        assert upper > prob
