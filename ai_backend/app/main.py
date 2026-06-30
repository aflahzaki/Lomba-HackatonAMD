"""LangkahKampus AI Backend - FastAPI application."""

from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .models.predictor import predictor
from .schemas.prediction import (
    AdvisorRequest,
    AdvisorResponse,
    PredictionRequest,
    PredictionResponse,
    RecommendRequest,
    RecommendResponse,
    VariableBreakdown,
)
from .services.advisor import get_advisor_response
from .services.recommender import get_recommendations

app = FastAPI(
    title="LangkahKampus AI Backend",
    description="AI-powered SNBP admission prediction with ML model and LLM advisor",
    version="1.0.0",
)

# CORS middleware
# Note: allow_credentials=False because the PHP frontend communicates via
# server-side cURL (not browser CORS requests). allow_origins=["*"] with
# allow_credentials=True is invalid per the CORS spec.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Load ML model and SIDATA data on startup."""
    predictor.load_sidata()
    predictor.load_model()


@app.get("/api/health")
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


@app.post("/api/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    ML-based prediction of SNBP acceptance probability.

    Uses trained XGBoost model with fallback to deterministic formula.
    """
    # Calculate average score from scores dict
    total_score = 0.0
    score_count = 0

    try:
        for subject, semesters in request.scores.items():
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
    ranking_percentile = request.school_ranking / request.total_students

    # Find target program in SIDATA
    program = predictor.sidata.find_program(request.target_program_id)

    # Get prediction
    probability, confidence_lower, confidence_upper = predictor.predict(
        avg_score=avg_score,
        ranking_percentile=ranking_percentile,
        accreditation=request.school_accreditation,
        program=program,
    )

    # Get variable breakdown
    variables_raw = predictor.get_variable_breakdown(
        avg_score=avg_score,
        ranking=request.school_ranking,
        total_students=request.total_students,
        accreditation=request.school_accreditation,
        program=program,
    )
    variables = [VariableBreakdown(**v) for v in variables_raw]

    # Get recommendations (top 3)
    recommendations = get_recommendations(
        target_program_id=request.target_program_id,
        avg_score=avg_score,
        ranking_percentile=ranking_percentile,
        accreditation=request.school_accreditation,
        limit=3,
    )

    program_name = program["nama_prodi"] if program else request.target_program_id
    program_univ = program.get("nama_univ", "") if program else ""

    return PredictionResponse(
        success=True,
        probability=round(probability * 100, 1),
        confidence_lower=round(confidence_lower, 4),
        confidence_upper=round(confidence_upper, 4),
        variables=variables,
        recommendations=recommendations,
        input_summary={
            "avg_score": round(avg_score, 2),
            "ranking": f"{request.school_ranking}/{request.total_students}",
            "school_accreditation": request.school_accreditation,
            "target_program": program_name,
            "target_university": program_univ,
            "jurusan": request.jurusan or "",
        },
        timestamp=datetime.now().isoformat(),
    )


@app.post("/api/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest):
    """Get smart program recommendations based on student profile."""
    # Calculate average score
    total_score = 0.0
    score_count = 0

    try:
        for subject, semesters in request.scores.items():
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
    ranking_percentile = request.school_ranking / request.total_students

    program = predictor.sidata.find_program(request.target_program_id)
    target_name = program["nama_prodi"] if program else request.target_program_id

    recommendations = get_recommendations(
        target_program_id=request.target_program_id,
        avg_score=avg_score,
        ranking_percentile=ranking_percentile,
        accreditation=request.school_accreditation,
        limit=request.limit,
    )

    return RecommendResponse(
        success=True,
        target_program=target_name,
        recommendations=recommendations,
    )


@app.post("/api/advisor", response_model=AdvisorResponse)
async def advisor(request: AdvisorRequest):
    """AI advisor chatbot powered by Fireworks AI."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    result = await get_advisor_response(
        message=request.message,
        context=request.context,
        history=request.history,
    )

    return AdvisorResponse(
        reply=result["reply"],
        suggestions=result.get("suggestions", []),
    )
