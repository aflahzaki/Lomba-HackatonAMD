"""Tests for generate_reference_images.py color constants and chart functions."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from generate_reference_images import (
    DARK_BLUE,
    ACCENT_BLUE,
    LIGHT_BLUE,
    RED,
    GREEN,
    ORANGE,
    GRAY,
    LIGHT_GRAY,
    generate_snbp_acceptance_chart,
    generate_ml_model_comparison,
    generate_tam_sam_som,
    generate_xai_framework_comparison,
    generate_market_validation_chart,
)


class TestColorConstants:
    def test_dark_blue_is_hex(self):
        assert DARK_BLUE.startswith("#")
        assert len(DARK_BLUE) == 7

    def test_accent_blue_is_hex(self):
        assert ACCENT_BLUE.startswith("#")
        assert len(ACCENT_BLUE) == 7

    def test_light_blue_is_hex(self):
        assert LIGHT_BLUE.startswith("#")

    def test_red_is_hex(self):
        assert RED.startswith("#")

    def test_green_is_hex(self):
        assert GREEN.startswith("#")

    def test_orange_is_hex(self):
        assert ORANGE.startswith("#")

    def test_gray_is_hex(self):
        assert GRAY.startswith("#")

    def test_light_gray_is_hex(self):
        assert LIGHT_GRAY.startswith("#")

    def test_all_colors_valid_hex(self):
        for color in [DARK_BLUE, ACCENT_BLUE, LIGHT_BLUE, RED, GREEN, ORANGE, GRAY, LIGHT_GRAY]:
            hex_part = color[1:]
            int(hex_part, 16)  # should not raise


class TestChartGeneration:
    """Verify chart functions run without errors and produce figure files."""

    def setup_method(self):
        plt.close("all")

    def teardown_method(self):
        plt.close("all")

    def test_snbp_acceptance_chart(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "generate_reference_images.OUTPUT_DIR", str(tmp_path)
        )
        generate_snbp_acceptance_chart()
        files = list(tmp_path.iterdir())
        assert len(files) >= 1
        assert any(f.suffix == ".png" for f in files)

    def test_ml_model_comparison(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "generate_reference_images.OUTPUT_DIR", str(tmp_path)
        )
        generate_ml_model_comparison()
        files = list(tmp_path.iterdir())
        assert len(files) >= 1

    def test_tam_sam_som(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "generate_reference_images.OUTPUT_DIR", str(tmp_path)
        )
        generate_tam_sam_som()
        files = list(tmp_path.iterdir())
        assert len(files) >= 1

    def test_xai_framework_comparison(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "generate_reference_images.OUTPUT_DIR", str(tmp_path)
        )
        generate_xai_framework_comparison()
        files = list(tmp_path.iterdir())
        assert len(files) >= 1

    def test_market_validation_chart(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "generate_reference_images.OUTPUT_DIR", str(tmp_path)
        )
        generate_market_validation_chart()
        files = list(tmp_path.iterdir())
        assert len(files) >= 1

    def test_chart_output_is_png(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "generate_reference_images.OUTPUT_DIR", str(tmp_path)
        )
        generate_snbp_acceptance_chart()
        png_files = [f for f in tmp_path.iterdir() if f.suffix == ".png"]
        assert len(png_files) >= 1
        for f in png_files:
            assert f.stat().st_size > 0
