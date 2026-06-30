"""SHAP-based model explainability service."""

from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..models.predictor import predictor

# Feature names in model input order
FEATURE_NAMES = [
    "avg_score",
    "ranking_percentile",
    "accred_score",
    "competition_ratio",
    "applicant_trend",
    "daya_tampung",
]

# Human-readable Indonesian feature labels
FEATURE_LABELS = {
    "avg_score": "Nilai Rata-rata",
    "ranking_percentile": "Persentil Peringkat",
    "accred_score": "Skor Akreditasi Sekolah",
    "competition_ratio": "Rasio Kompetisi Program",
    "applicant_trend": "Tren Peminat",
    "daya_tampung": "Daya Tampung",
}


def _get_feature_description(feature_name: str, value: float, contribution: float) -> str:
    """Generate human-readable explanation in Indonesian for a feature contribution."""
    label = FEATURE_LABELS.get(feature_name, feature_name)
    direction = "meningkatkan" if contribution > 0 else "menurunkan"
    abs_contrib = abs(contribution)

    if feature_name == "avg_score":
        return (
            f"{label} ({value:.1f}) {direction} peluang sebesar "
            f"{abs_contrib:.3f}"
        )
    elif feature_name == "ranking_percentile":
        pct = value * 100
        return (
            f"{label} (top {pct:.0f}%) {direction} peluang sebesar "
            f"{abs_contrib:.3f}"
        )
    elif feature_name == "accred_score":
        accred_label = "A" if value >= 0.9 else "B" if value >= 0.6 else "C" if value >= 0.3 else "Lainnya"
        return (
            f"{label} (Akreditasi {accred_label}) {direction} peluang sebesar "
            f"{abs_contrib:.3f}"
        )
    elif feature_name == "competition_ratio":
        return (
            f"{label} ({value:.1f}:1) {direction} peluang sebesar "
            f"{abs_contrib:.3f}"
        )
    elif feature_name == "applicant_trend":
        trend_dir = "naik" if value > 0 else "turun"
        return (
            f"{label} ({trend_dir} {abs(value)*100:.1f}%) {direction} peluang sebesar "
            f"{abs_contrib:.3f}"
        )
    elif feature_name == "daya_tampung":
        return (
            f"{label} ({int(value)} kursi) {direction} peluang sebesar "
            f"{abs_contrib:.3f}"
        )
    else:
        return f"{label} ({value:.2f}) {direction} peluang sebesar {abs_contrib:.3f}"


def compute_shap_values(
    features: np.ndarray,
) -> Tuple[List[float], float]:
    """
    Compute SHAP values for a single prediction.

    Args:
        features: numpy array of shape (1, 6) with feature values

    Returns:
        Tuple of (shap_values_list, base_value)
    """
    model = predictor.model

    if model is None or not predictor.model_loaded:
        # Fallback: use deterministic weights as pseudo-SHAP values
        return _fallback_importance(features)

    try:
        import shap

        # Try TreeExplainer for tree-based models (XGBoost, sklearn trees)
        explainer = shap.TreeExplainer(model)
        shap_result = explainer.shap_values(features)

        # Handle different SHAP output formats
        if isinstance(shap_result, list):
            # For multi-class, take the positive class
            shap_vals = shap_result[1][0] if len(shap_result) > 1 else shap_result[0][0]
        elif hasattr(shap_result, 'values'):
            shap_vals = shap_result.values[0]
        else:
            shap_vals = shap_result[0]

        base_value = explainer.expected_value
        if isinstance(base_value, (list, np.ndarray)):
            base_value = float(base_value[1]) if len(base_value) > 1 else float(base_value[0])
        else:
            base_value = float(base_value)

        return [float(v) for v in shap_vals], base_value

    except Exception:
        # Fallback if SHAP computation fails
        return _fallback_importance(features)


def _fallback_importance(features: np.ndarray) -> Tuple[List[float], float]:
    """
    Fallback: compute pseudo-SHAP values using model feature importances
    or deterministic weights when SHAP is unavailable.

    Returns:
        Tuple of (importance_values, base_value)
    """
    model = predictor.model
    base_value = 0.5  # default base

    if model is not None and hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        # Scale importances by feature deviations from a baseline
        baseline = np.array([[80.0, 0.5, 0.7, 10.0, 0.0, 100.0]])
        deviations = features[0] - baseline[0]
        # Pseudo-SHAP: importance * sign of deviation * magnitude factor
        pseudo_shap = []
        for i, (imp, dev) in enumerate(zip(importances, deviations)):
            # Normalize deviation relative to baseline
            base_val = max(abs(baseline[0][i]), 1.0)
            normalized_dev = dev / base_val
            pseudo_shap.append(float(imp * normalized_dev * 0.5))
        return pseudo_shap, base_value
    else:
        # Pure deterministic weights fallback
        weights = np.array([0.25, 0.20, 0.10, 0.30, 0.10, 0.05])
        baseline = np.array([80.0, 0.5, 0.7, 10.0, 0.0, 100.0])
        deviations = features[0] - baseline[0]
        pseudo_shap = []
        for i, (w, dev) in enumerate(zip(weights, deviations)):
            base_val = max(abs(baseline[0][i]), 1.0)
            normalized_dev = dev / base_val
            pseudo_shap.append(float(w * normalized_dev * 0.5))
        return pseudo_shap, base_value


def explain_prediction(
    avg_score: float,
    ranking_percentile: float,
    accreditation: str,
    program: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generate SHAP explanation for a prediction.

    Returns dict with shap_values, base_value, prediction, explanation_text.

    NOTE: Known trade-off for hackathon -- feature vector is reconstructed here
    independently of predictor.predict(). If predictor feature engineering
    changes (e.g., new features or normalization), this must be updated in sync.
    A shared _build_features() helper would eliminate drift risk in production.
    """
    # Compute program features (same logic as predictor.predict)
    if program:
        competition_ratio = program["peminat_2022"] / max(
            program["daya_tampung_2022"], 1
        )
        peminat_2018 = max(program["peminat_2018"], 1)
        applicant_trend = (program["peminat_2022"] - peminat_2018) / peminat_2018
        daya_tampung = program["daya_tampung_2023"]
    else:
        competition_ratio = 15.0
        applicant_trend = 0.0
        daya_tampung = 50

    # Encode accreditation
    accred_map = {"A": 1.0, "B": 0.7, "C": 0.4}
    accred_score = accred_map.get(accreditation.upper(), 0.2)

    features = np.array(
        [[avg_score, ranking_percentile, accred_score, competition_ratio, applicant_trend, daya_tampung]]
    )

    # Get prediction
    probability, _, _ = predictor.predict(
        avg_score=avg_score,
        ranking_percentile=ranking_percentile,
        accreditation=accreditation,
        program=program,
    )

    # Get SHAP values
    shap_vals, base_value = compute_shap_values(features)

    # Build feature contributions sorted by absolute impact
    contributions = []
    for i, (name, val, contrib) in enumerate(zip(FEATURE_NAMES, features[0], shap_vals)):
        contributions.append({
            "feature": name,
            "value": float(val),
            "contribution": float(contrib),
            "description": _get_feature_description(name, float(val), float(contrib)),
        })

    # Sort by absolute contribution descending
    contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)

    # Generate summary explanation text in Indonesian
    top_positive = [c for c in contributions if c["contribution"] > 0]
    top_negative = [c for c in contributions if c["contribution"] < 0]

    explanation_parts = []
    if top_positive:
        pos_names = [FEATURE_LABELS[c["feature"]] for c in top_positive[:2]]
        explanation_parts.append(
            f"Faktor yang paling mendukung peluang Anda: {', '.join(pos_names)}"
        )
    if top_negative:
        neg_names = [FEATURE_LABELS[c["feature"]] for c in top_negative[:2]]
        explanation_parts.append(
            f"Faktor yang perlu ditingkatkan: {', '.join(neg_names)}"
        )

    explanation_text = ". ".join(explanation_parts) + "." if explanation_parts else "Tidak ada faktor dominan yang teridentifikasi."

    return {
        "shap_values": contributions,
        "base_value": float(base_value),
        "prediction": float(probability),
        "explanation_text": explanation_text,
    }
