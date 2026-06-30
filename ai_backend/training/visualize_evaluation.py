"""
Model Evaluation Visualization for LangkahKampus.

Generates publication-quality evaluation charts as PNG files
for presentation slides and competition submission materials.

Charts generated:
1. Feature Importance (horizontal bar chart)
2. Actual vs Predicted (scatter plot)
3. Prediction Distribution (histogram overlay)
4. Residual Plot (residuals vs predicted)

All charts are saved to ai_backend/training/evaluation_charts/
"""

import os
import sys

import joblib
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend (no display needed)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# Paths
TRAINING_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "training_data.csv",
)

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "models",
    "prediction_model.joblib",
)

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "evaluation_charts",
)

FEATURE_COLS = [
    "avg_score",
    "ranking_percentile",
    "accred_score",
    "competition_ratio",
    "applicant_trend",
    "daya_tampung",
]

FEATURE_LABELS = {
    "avg_score": "Nilai Rata-rata",
    "ranking_percentile": "Peringkat (Persentil)",
    "accred_score": "Skor Akreditasi",
    "competition_ratio": "Rasio Kompetisi",
    "applicant_trend": "Tren Pendaftar",
    "daya_tampung": "Daya Tampung",
}

TARGET_COL = "probability"

# Chart styling
BRAND_COLOR = "#E4002B"  # AMD Red
BRAND_SECONDARY = "#1A1A2E"
CHART_PALETTE = ["#E4002B", "#0071C5", "#76B900", "#FF6F00", "#7B1FA2", "#00ACC1"]


def setup_style():
    """Configure matplotlib/seaborn for publication-quality output."""
    sns.set_theme(style="whitegrid", font_scale=1.1)
    plt.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 150,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
    })


def plot_feature_importance(model, output_path):
    """Generate feature importance horizontal bar chart."""
    importances = model.feature_importances_
    labels = [FEATURE_LABELS.get(f, f) for f in FEATURE_COLS]

    # Sort by importance
    indices = np.argsort(importances)
    sorted_labels = [labels[i] for i in indices]
    sorted_importances = importances[indices]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(sorted_labels, sorted_importances, color=CHART_PALETTE[:len(FEATURE_COLS)])
    ax.set_xlabel("Importance Score")
    ax.set_title("LangkahKampus - Feature Importance\n(XGBoost Model trained on AMD GPU)")
    ax.set_xlim(0, max(sorted_importances) * 1.15)

    # Add value labels on bars
    for bar, val in zip(bars, sorted_importances):
        ax.text(
            bar.get_width() + 0.005,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.3f}",
            va="center",
            fontsize=10,
        )

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


def plot_actual_vs_predicted(y_actual, y_predicted, output_path):
    """Generate actual vs predicted scatter plot."""
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.scatter(
        y_actual * 100,
        y_predicted * 100,
        alpha=0.3,
        s=20,
        color=BRAND_COLOR,
        edgecolors="none",
    )

    # Perfect prediction line
    min_val = min(y_actual.min(), y_predicted.min()) * 100
    max_val = max(y_actual.max(), y_predicted.max()) * 100
    ax.plot(
        [min_val, max_val],
        [min_val, max_val],
        "k--",
        linewidth=1.5,
        alpha=0.7,
        label="Perfect Prediction",
    )

    r2 = r2_score(y_actual, y_predicted)
    mae = mean_absolute_error(y_actual, y_predicted) * 100

    ax.set_xlabel("Actual Probability (%)")
    ax.set_ylabel("Predicted Probability (%)")
    ax.set_title(
        f"LangkahKampus - Actual vs Predicted (Test Set)\n"
        f"R2 = {r2:.4f} | MAE = {mae:.2f}%"
    )
    ax.legend(loc="upper left")
    ax.set_aspect("equal", adjustable="box")

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


def plot_prediction_distribution(y_actual, y_predicted, output_path):
    """Generate prediction distribution histogram (actual vs predicted overlay)."""
    fig, ax = plt.subplots(figsize=(10, 6))

    bins = np.linspace(0, 1, 30)

    ax.hist(
        y_actual * 100,
        bins=bins * 100,
        alpha=0.5,
        label="Actual",
        color=BRAND_COLOR,
        edgecolor="white",
    )
    ax.hist(
        y_predicted * 100,
        bins=bins * 100,
        alpha=0.5,
        label="Predicted",
        color="#0071C5",
        edgecolor="white",
    )

    ax.set_xlabel("Probability (%)")
    ax.set_ylabel("Count")
    ax.set_title("LangkahKampus - Prediction Distribution (Test Set)\n(Actual vs Predicted)")
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


def plot_residuals(y_actual, y_predicted, output_path):
    """Generate residual plot (residuals vs predicted values)."""
    residuals = (y_actual - y_predicted) * 100
    predicted_pct = y_predicted * 100

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        predicted_pct,
        residuals,
        alpha=0.3,
        s=20,
        color=BRAND_COLOR,
        edgecolors="none",
    )
    ax.axhline(y=0, color="black", linestyle="--", linewidth=1)

    # Add std deviation bands
    std_res = np.std(residuals)
    ax.axhline(y=std_res, color="#0071C5", linestyle=":", alpha=0.5, label=f"+1 SD ({std_res:.2f}%)")
    ax.axhline(y=-std_res, color="#0071C5", linestyle=":", alpha=0.5, label=f"-1 SD ({-std_res:.2f}%)")

    ax.set_xlabel("Predicted Probability (%)")
    ax.set_ylabel("Residual (Actual - Predicted) (%)")
    ax.set_title("LangkahKampus - Residual Plot (Test Set)\n(Model Error Analysis)")
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


def main():
    """Generate all evaluation charts."""
    print("=" * 60)
    print("LangkahKampus - Model Evaluation Visualization")
    print("=" * 60)

    # Load model
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model not found at {MODEL_PATH}")
        print("Run train_model.py or train_on_amd_cloud.py first.")
        sys.exit(1)

    model = joblib.load(MODEL_PATH)
    print(f"Model loaded: {type(model).__name__}")

    # Load data
    if not os.path.exists(TRAINING_DATA_PATH):
        print(f"ERROR: Training data not found at {TRAINING_DATA_PATH}")
        sys.exit(1)

    df = pd.read_csv(TRAINING_DATA_PATH)
    print(f"Data loaded: {len(df)} samples")

    X = df[FEATURE_COLS].values
    y = df[TARGET_COL].values

    # Use a held-out test set (80/20 split) for honest evaluation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Train/Test split: {len(X_train)} train, {len(X_test)} test samples")

    # Generate predictions on the TEST set only
    y_pred = np.clip(model.predict(X_test), 0.05, 0.95)

    # Setup output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\nOutput directory: {OUTPUT_DIR}")

    # Setup style
    setup_style()

    # Generate charts
    print("\nGenerating charts...")

    plot_feature_importance(
        model,
        os.path.join(OUTPUT_DIR, "feature_importance.png"),
    )

    plot_actual_vs_predicted(
        y_test, y_pred,
        os.path.join(OUTPUT_DIR, "actual_vs_predicted.png"),
    )

    plot_prediction_distribution(
        y_test, y_pred,
        os.path.join(OUTPUT_DIR, "prediction_distribution.png"),
    )

    plot_residuals(
        y_test, y_pred,
        os.path.join(OUTPUT_DIR, "residual_plot.png"),
    )

    print(f"\n{'='*60}")
    print("All charts generated successfully!")
    print(f"Charts saved to: {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
