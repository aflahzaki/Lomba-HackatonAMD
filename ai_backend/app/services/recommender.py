"""Smart recommendation service for alternative programs."""

from typing import Any, Dict, List, Optional

from ..models.predictor import predictor
from ..schemas.prediction import Recommendation


def get_recommendations(
    target_program_id: str,
    avg_score: float,
    ranking_percentile: float,
    accreditation: str,
    limit: int = 5,
) -> List[Recommendation]:
    """
    Find similar programs with lower competition ratios.

    If the ML model is available, also predict probability for each alternative.
    """
    target_program = predictor.sidata.find_program(target_program_id)
    if not target_program:
        return []

    similar_programs = predictor.sidata.find_similar_programs(target_program, limit=limit)

    target_ratio = target_program["peminat_2022"] / max(
        target_program["daya_tampung_2022"], 1
    )

    recommendations = []
    for prog in similar_programs:
        ratio = prog["peminat_2022"] / max(prog["daya_tampung_2022"], 1)

        # Predict probability for this alternative if model is available
        predicted_prob = None
        if predictor.model_loaded:
            prob, _, _ = predictor.predict(
                avg_score=avg_score,
                ranking_percentile=ranking_percentile,
                accreditation=accreditation,
                program=prog,
            )
            predicted_prob = round(prob * 100, 1)

        recommendations.append(
            Recommendation(
                name=prog["nama_prodi"],
                university=prog.get("nama_univ", ""),
                ratio=round(ratio, 1),
                daya_tampung=prog["daya_tampung_2023"],
                comparison=f"Rasio {ratio:.1f}:1 vs {target_ratio:.1f}:1",
                predicted_probability=predicted_prob,
            )
        )

    return recommendations
