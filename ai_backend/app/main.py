"""LangkahKampus AI Backend - FastAPI application."""

import time
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from .config import settings
from .middleware.error_handler import global_exception_handler
from .middleware.logging import StructuredLoggingMiddleware
from .middleware.metrics import metrics
from .middleware.rate_limiter import limiter, rate_limit_exceeded_handler
from .middleware.security import SecurityHeadersMiddleware
from .models.predictor import predictor
from .schemas.prediction import (
    AdvisorRequest,
    AdvisorResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    BatchPredictionSummary,
    ExplainRequest,
    ExplainResponse,
    FeatureContribution,
    PredictionRequest,
    PredictionResponse,
    RecommendRequest,
    RecommendResponse,
    VariableBreakdown,
    WhatIfRequest,
    WhatIfResponse,
)
from .services.advisor import get_advisor_response
from .services.explainer import explain_prediction
from .services.recommender import get_recommendations

# OpenAPI tag metadata
tags_metadata = [
    {
        "name": "Prediction",
        "description": "ML-based SNBP acceptance probability prediction endpoints.",
    },
    {
        "name": "Recommendation",
        "description": "Smart program recommendation based on student profile.",
    },
    {
        "name": "Advisor",
        "description": "AI-powered academic advisor chatbot.",
    },
    {
        "name": "Monitoring",
        "description": "Health checks, metrics, and operational monitoring.",
    },
    {
        "name": "Explainability",
        "description": "Model explainability and transparency endpoints.",
    },
]

app = FastAPI(
    title="LangkahKampus AI Backend",
    description="AI-powered SNBP admission prediction with ML model and LLM advisor",
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "LangkahKampus Team",
        "url": "https://github.com/aflahzaki/Lomba-HackatonAMD",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Register rate limiter state
app.state.limiter = limiter

# Register exception handlers
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Middleware order: security headers first, then logging, then CORS
# (added in reverse since Starlette processes middleware in LIFO order)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(StructuredLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


@app.on_event("startup")
async def startup_event():
    """Load ML model and SIDATA data on startup."""
    predictor.load_sidata()
    predictor.load_model()
    # Reset metrics start time on actual startup
    metrics.start_time = time.time()


@app.get("/api/health", tags=["Monitoring"])
async def health_check():
    """Health check endpoint with model status."""
    return {
        "status": "healthy",
        "model_loaded": predictor.model_loaded,
        "sidata_loaded": predictor.sidata.is_loaded,
        "sidata_programs": len(predictor.sidata.programs),
        "sidata_universities": len(predictor.sidata.universities),
        "advisor_configured": bool(settings.FIREWORKS_API_KEY),
    }


@app.get("/api/metrics", tags=["Monitoring"])
async def get_metrics():
    """Return application metrics for monitoring."""
    return metrics.get_metrics()


@app.post("/api/predict", response_model=PredictionResponse, tags=["Prediction"])
@limiter.limit("30/minute")
async def predict(request: Request, body: PredictionRequest):
    """
    ML-based prediction of SNBP acceptance probability.

    Uses trained XGBoost model with fallback to deterministic formula.
    """
    # Calculate average score from scores dict
    total_score = 0.0
    score_count = 0

    try:
        for subject, semesters in body.scores.items():
            if isinstance(semesters, dict):
                for sem, score in semesters.items():
                    val = float(score)
                    if val > 0:
                        total_score += val
                        score_count += 1
            else:
                # Handle case where scores is flat {subject: score}
                val = float(semesters)
                if val > 0:
                    total_score += val
                    score_count += 1
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=422,
            detail=[{"msg": f"Invalid score value: all scores must be numeric. Error: {str(e)}", "type": "value_error"}],
        )

    avg_score = total_score / score_count if score_count > 0 else 75.0
    ranking_percentile = body.school_ranking / body.total_students

    # Find target program in SIDATA
    program = predictor.sidata.find_program(body.target_program_id)

    # Get prediction
    probability, confidence_lower, confidence_upper = predictor.predict(
        avg_score=avg_score,
        ranking_percentile=ranking_percentile,
        accreditation=body.school_accreditation,
        program=program,
    )

    # Get variable breakdown
    variables_raw = predictor.get_variable_breakdown(
        avg_score=avg_score,
        ranking=body.school_ranking,
        total_students=body.total_students,
        accreditation=body.school_accreditation,
        program=program,
    )
    variables = [VariableBreakdown(**v) for v in variables_raw]

    # Get recommendations (top 3)
    recommendations = get_recommendations(
        target_program_id=body.target_program_id,
        avg_score=avg_score,
        ranking_percentile=ranking_percentile,
        accreditation=body.school_accreditation,
        limit=3,
    )

    program_name = program["nama_prodi"] if program else body.target_program_id
    program_univ = program.get("nama_univ", "") if program else ""

    # Record prediction in metrics
    metrics.record_prediction(program_name)

    return PredictionResponse(
        success=True,
        probability=round(probability * 100, 1),
        confidence_lower=round(confidence_lower, 4),
        confidence_upper=round(confidence_upper, 4),
        variables=variables,
        recommendations=recommendations,
        input_summary={
            "avg_score": round(avg_score, 2),
            "ranking": f"{body.school_ranking}/{body.total_students}",
            "school_accreditation": body.school_accreditation,
            "target_program": program_name,
            "target_university": program_univ,
            "jurusan": body.jurusan or "",
        },
        timestamp=datetime.now().isoformat(),
    )


@app.post("/api/recommend", response_model=RecommendResponse, tags=["Recommendation"])
@limiter.limit("60/minute")
async def recommend(request: Request, body: RecommendRequest):
    """Get smart program recommendations based on student profile."""
    # Calculate average score
    total_score = 0.0
    score_count = 0

    try:
        for subject, semesters in body.scores.items():
            if isinstance(semesters, dict):
                for sem, score in semesters.items():
                    val = float(score)
                    if val > 0:
                        total_score += val
                        score_count += 1
            else:
                val = float(semesters)
                if val > 0:
                    total_score += val
                    score_count += 1
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=422,
            detail=[{"msg": f"Invalid score value: all scores must be numeric. Error: {str(e)}", "type": "value_error"}],
        )

    avg_score = total_score / score_count if score_count > 0 else 75.0
    ranking_percentile = body.school_ranking / body.total_students

    program = predictor.sidata.find_program(body.target_program_id)
    target_name = program["nama_prodi"] if program else body.target_program_id

    recommendations = get_recommendations(
        target_program_id=body.target_program_id,
        avg_score=avg_score,
        ranking_percentile=ranking_percentile,
        accreditation=body.school_accreditation,
        limit=body.limit,
    )

    return RecommendResponse(
        success=True,
        target_program=target_name,
        recommendations=recommendations,
    )


@app.post("/api/advisor", response_model=AdvisorResponse, tags=["Advisor"])
@limiter.limit("10/minute")
async def advisor(request: Request, body: AdvisorRequest):
    """AI advisor chatbot powered by Fireworks AI."""
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    result = await get_advisor_response(
        message=body.message,
        context=body.context,
        history=body.history,
    )

    return AdvisorResponse(
        reply=result["reply"],
        suggestions=result.get("suggestions", []),
    )


@app.post("/api/explain", response_model=ExplainResponse, tags=["Explainability"])
@limiter.limit("30/minute")
async def explain(request: Request, body: ExplainRequest):
    """
    SHAP model explainability endpoint.

    Returns per-feature contribution values sorted by absolute impact,
    with human-readable explanations in Indonesian.
    """
    # Calculate average score from scores dict
    total_score = 0.0
    score_count = 0

    try:
        for subject, semesters in body.scores.items():
            if isinstance(semesters, dict):
                for sem, score in semesters.items():
                    val = float(score)
                    if val > 0:
                        total_score += val
                        score_count += 1
            else:
                val = float(semesters)
                if val > 0:
                    total_score += val
                    score_count += 1
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=422,
            detail=[{"msg": f"Invalid score value: all scores must be numeric. Error: {str(e)}", "type": "value_error"}],
        )

    avg_score = total_score / score_count if score_count > 0 else 75.0
    ranking_percentile = body.school_ranking / body.total_students

    # Find target program in SIDATA
    program = predictor.sidata.find_program(body.target_program_id)

    # Get SHAP explanation
    result = explain_prediction(
        avg_score=avg_score,
        ranking_percentile=ranking_percentile,
        accreditation=body.school_accreditation,
        program=program,
    )

    # Record metrics
    metrics.record_explain()

    return ExplainResponse(
        success=True,
        shap_values=[FeatureContribution(**sv) for sv in result["shap_values"]],
        base_value=result["base_value"],
        prediction=result["prediction"],
        explanation_text=result["explanation_text"],
    )


@app.post("/api/predict/batch", response_model=BatchPredictionResponse, tags=["Prediction"])
@limiter.limit("30/minute")
async def predict_batch(request: Request, body: BatchPredictionRequest):
    """
    Batch prediction for teachers (guru BK).

    Accepts array of students (max 50), returns array of predictions with summary stats.
    """
    results = []

    for student in body.students:
        # Calculate average score
        total_score = 0.0
        score_count = 0

        try:
            for subject, semesters in student.scores.items():
                if isinstance(semesters, dict):
                    for sem, score in semesters.items():
                        val = float(score)
                        if val > 0:
                            total_score += val
                            score_count += 1
                else:
                    val = float(semesters)
                    if val > 0:
                        total_score += val
                        score_count += 1
        except (ValueError, TypeError) as e:
            raise HTTPException(
                status_code=422,
                detail=[{"msg": f"Invalid score value: all scores must be numeric. Error: {str(e)}", "type": "value_error"}],
            )

        avg_score = total_score / score_count if score_count > 0 else 75.0
        ranking_percentile = student.school_ranking / student.total_students

        # Find target program
        program = predictor.sidata.find_program(student.target_program_id)

        # Get prediction
        probability, confidence_lower, confidence_upper = predictor.predict(
            avg_score=avg_score,
            ranking_percentile=ranking_percentile,
            accreditation=student.school_accreditation,
            program=program,
        )

        # Get variable breakdown
        variables_raw = predictor.get_variable_breakdown(
            avg_score=avg_score,
            ranking=student.school_ranking,
            total_students=student.total_students,
            accreditation=student.school_accreditation,
            program=program,
        )
        variables = [VariableBreakdown(**v) for v in variables_raw]

        # Get recommendations
        recommendations = get_recommendations(
            target_program_id=student.target_program_id,
            avg_score=avg_score,
            ranking_percentile=ranking_percentile,
            accreditation=student.school_accreditation,
            limit=3,
        )

        program_name = program["nama_prodi"] if program else student.target_program_id
        program_univ = program.get("nama_univ", "") if program else ""

        # Record prediction in metrics
        metrics.record_prediction(program_name)

        results.append(PredictionResponse(
            success=True,
            probability=round(probability * 100, 1),
            confidence_lower=round(confidence_lower, 4),
            confidence_upper=round(confidence_upper, 4),
            variables=variables,
            recommendations=recommendations,
            input_summary={
                "avg_score": round(avg_score, 2),
                "ranking": f"{student.school_ranking}/{student.total_students}",
                "school_accreditation": student.school_accreditation,
                "target_program": program_name,
                "target_university": program_univ,
                "jurusan": student.jurusan or "",
            },
            timestamp=datetime.now().isoformat(),
        ))

    # Compute summary stats
    probabilities = [r.probability for r in results]
    summary = BatchPredictionSummary(
        count=len(results),
        avg_probability=round(sum(probabilities) / len(probabilities), 1),
        highest=max(probabilities),
        lowest=min(probabilities),
    )

    # Record batch metrics
    metrics.record_batch(len(results))

    return BatchPredictionResponse(
        success=True,
        results=results,
        summary=summary,
    )


@app.post("/api/what-if", response_model=WhatIfResponse, tags=["Explainability"])
@limiter.limit("30/minute")
async def what_if(request: Request, body: WhatIfRequest):
    """
    What-if analysis endpoint.

    Student changes one variable and sees how the probability changes.
    Returns original probability, new probability, change delta, and insight in Indonesian.
    """
    # Calculate average score from scores dict
    total_score = 0.0
    score_count = 0

    try:
        for subject, semesters in body.scores.items():
            if isinstance(semesters, dict):
                for sem, score in semesters.items():
                    val = float(score)
                    if val > 0:
                        total_score += val
                        score_count += 1
            else:
                val = float(semesters)
                if val > 0:
                    total_score += val
                    score_count += 1
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=422,
            detail=[{"msg": f"Invalid score value: all scores must be numeric. Error: {str(e)}", "type": "value_error"}],
        )

    avg_score = total_score / score_count if score_count > 0 else 75.0
    ranking_percentile = body.school_ranking / body.total_students

    # Find target program
    program = predictor.sidata.find_program(body.target_program_id)

    # Compute original prediction
    original_prob, _, _ = predictor.predict(
        avg_score=avg_score,
        ranking_percentile=ranking_percentile,
        accreditation=body.school_accreditation,
        program=program,
    )
    original_probability = round(original_prob * 100, 1)

    # Apply the what-if change
    new_avg_score = avg_score
    new_ranking_percentile = ranking_percentile
    new_accreditation = body.school_accreditation
    new_program = program

    variable = body.variable_to_change
    new_value = body.new_value

    if variable == "avg_score":
        try:
            new_avg_score = float(new_value)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=422,
                detail=[{"msg": "new_value untuk avg_score harus berupa angka", "type": "value_error"}],
            )
    elif variable == "school_ranking":
        try:
            new_ranking = int(float(new_value))
            new_ranking_percentile = new_ranking / body.total_students
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=422,
                detail=[{"msg": "new_value untuk school_ranking harus berupa angka bulat", "type": "value_error"}],
            )
    elif variable == "school_accreditation":
        new_accreditation = new_value.strip().upper()
        if new_accreditation not in ("A", "B", "C"):
            raise HTTPException(
                status_code=422,
                detail=[{"msg": "new_value untuk school_accreditation harus A, B, atau C", "type": "value_error"}],
            )
    elif variable == "target_program_id":
        new_program = predictor.sidata.find_program(new_value)

    # Compute new prediction
    new_prob, _, _ = predictor.predict(
        avg_score=new_avg_score,
        ranking_percentile=new_ranking_percentile,
        accreditation=new_accreditation,
        program=new_program,
    )
    new_probability = round(new_prob * 100, 1)

    change = round(new_probability - original_probability, 1)

    # Generate insight message in Indonesian
    insight = _generate_what_if_insight(variable, new_value, change)

    # Record metrics
    metrics.record_what_if()

    return WhatIfResponse(
        success=True,
        original_probability=original_probability,
        new_probability=new_probability,
        change=change,
        variable_changed=variable,
        insight=insight,
    )


def _generate_what_if_insight(variable: str, new_value: str, change: float) -> str:
    """Generate insight message in Indonesian for what-if analysis."""
    variable_labels = {
        "avg_score": "nilai rata-rata",
        "school_ranking": "peringkat sekolah",
        "school_accreditation": "akreditasi sekolah",
        "target_program_id": "program studi target",
    }
    var_label = variable_labels.get(variable, variable)

    if abs(change) < 0.5:
        return (
            f"Mengubah {var_label} menjadi {new_value} tidak memberikan "
            f"perubahan signifikan pada peluang Anda."
        )
    elif change > 0:
        return (
            f"Mengubah {var_label} menjadi {new_value} meningkatkan peluang Anda "
            f"sebesar {change:.1f} poin persentase. Ini adalah perubahan positif!"
        )
    else:
        return (
            f"Mengubah {var_label} menjadi {new_value} menurunkan peluang Anda "
            f"sebesar {abs(change):.1f} poin persentase. Pertimbangkan kembali perubahan ini."
        )
