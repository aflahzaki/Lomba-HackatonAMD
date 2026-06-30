"""
Model evaluation script.

Loads the trained model and runs comprehensive evaluation metrics.
"""

import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score

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

FEATURE_COLS = [
    "avg_score",
    "ranking_percentile",
    "accred_score",
    "competition_ratio",
    "applicant_trend",
    "daya_tampung",
]

TARGET_COL = "probability"


def main():
    """Run model evaluation."""
    print("=" * 60)
    print("LangkahKampus - Model Evaluation Report")
    print("=" * 60)

    # Load model
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model not found at {MODEL_PATH}")
        print("Run train_model.py first.")
        sys.exit(1)

    model = joblib.load(MODEL_PATH)
    print(f"Model loaded from: {MODEL_PATH}")
    print(f"Model type: {type(model).__name__}")

    # Load data
    if not os.path.exists(TRAINING_DATA_PATH):
        print(f"ERROR: Training data not found at {TRAINING_DATA_PATH}")
        sys.exit(1)

    df = pd.read_csv(TRAINING_DATA_PATH)
    print(f"Data loaded: {len(df)} samples")

    X = df[FEATURE_COLS].values
    y = df[TARGET_COL].values

    # Overall predictions
    y_pred = np.clip(model.predict(X), 0.05, 0.95)

    print(f"\n{'='*40}")
    print("OVERALL METRICS")
    print(f"{'='*40}")
    print(f"  MAE:  {mean_absolute_error(y, y_pred):.4f}")
    print(f"  RMSE: {np.sqrt(mean_squared_error(y, y_pred)):.4f}")
    print(f"  R2:   {r2_score(y, y_pred):.4f}")

    # Cross-validation
    print(f"\n{'='*40}")
    print("CROSS-VALIDATION (5-fold)")
    print(f"{'='*40}")
    cv_r2 = cross_val_score(model, X, y, cv=5, scoring="r2")
    cv_mae = -cross_val_score(model, X, y, cv=5, scoring="neg_mean_absolute_error")
    print(f"  R2:  {cv_r2.mean():.4f} (+/- {cv_r2.std() * 2:.4f})")
    print(f"  MAE: {cv_mae.mean():.4f} (+/- {cv_mae.std() * 2:.4f})")

    # Feature importances
    print(f"\n{'='*40}")
    print("FEATURE IMPORTANCES")
    print(f"{'='*40}")
    importances = model.feature_importances_
    for name, imp in sorted(
        zip(FEATURE_COLS, importances), key=lambda x: x[1], reverse=True
    ):
        bar = "#" * int(imp * 50)
        print(f"  {name:25s}: {imp:.4f} {bar}")

    # Prediction distribution analysis
    print(f"\n{'='*40}")
    print("PREDICTION DISTRIBUTION")
    print(f"{'='*40}")
    print(f"  Actual - mean: {y.mean():.4f}, std: {y.std():.4f}")
    print(f"  Predicted - mean: {y_pred.mean():.4f}, std: {y_pred.std():.4f}")

    # Test specific scenarios
    print(f"\n{'='*40}")
    print("SCENARIO TESTS")
    print(f"{'='*40}")

    scenarios = [
        ("Top student, easy program", [95, 0.05, 1.0, 3.0, -0.2, 100]),
        ("Average student, average program", [78, 0.5, 0.7, 10.0, 0.0, 50]),
        ("Below avg student, hard program", [65, 0.8, 0.4, 25.0, 0.5, 30]),
        ("Top student, hard program", [95, 0.05, 1.0, 25.0, 0.3, 30]),
        ("Average student, easy program", [78, 0.5, 0.7, 3.0, -0.1, 150]),
    ]

    for desc, features in scenarios:
        pred = model.predict([features])[0]
        pred = max(0.05, min(0.95, pred))
        print(f"  {desc:40s}: {pred*100:.1f}%")

    print(f"\n{'='*60}")
    print("Evaluation complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
