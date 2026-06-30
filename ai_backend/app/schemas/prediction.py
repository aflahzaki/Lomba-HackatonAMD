"""Pydantic schemas for request/response models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    """Request schema for prediction endpoint."""

    scores: Dict[str, Any] = Field(
        ..., description="Student scores as subject -> semester -> score mapping"
    )
    school_ranking: int = Field(..., ge=1, description="Student ranking in school")
    total_students: int = Field(..., ge=1, description="Total students in school")
    school_accreditation: str = Field(
        ..., description="School accreditation: A, B, or C"
    )
    target_program_id: str = Field(..., description="Target program name or ID")
    jurusan: Optional[str] = Field(None, description="Student major/track")


class VariableBreakdown(BaseModel):
    """Breakdown of a single prediction variable."""

    name: str
    weight: float
    raw_value: Any
    normalized_score: float
    description: str


class Recommendation(BaseModel):
    """A recommended alternative program."""

    name: str
    university: str
    ratio: float
    daya_tampung: int
    comparison: str
    predicted_probability: Optional[float] = None


class PredictionResponse(BaseModel):
    """Response schema for prediction endpoint."""

    success: bool = True
    probability: float = Field(..., ge=0, le=100)
    confidence_lower: float
    confidence_upper: float
    variables: List[VariableBreakdown]
    recommendations: List[Recommendation] = []
    input_summary: Dict[str, Any]
    timestamp: str


class RecommendRequest(BaseModel):
    """Request schema for recommendation endpoint."""

    scores: Dict[str, Any] = Field(
        ..., description="Student scores"
    )
    school_ranking: int = Field(..., ge=1)
    total_students: int = Field(..., ge=1)
    school_accreditation: str = Field(...)
    target_program_id: str = Field(..., description="Target program name or ID")
    jurusan: Optional[str] = None
    limit: int = Field(5, ge=1, le=20)


class RecommendResponse(BaseModel):
    """Response schema for recommendation endpoint."""

    success: bool = True
    target_program: str
    recommendations: List[Recommendation]


class AdvisorRequest(BaseModel):
    """Request schema for AI advisor endpoint."""

    message: str = Field(..., description="User message/question")
    context: Optional[Dict[str, Any]] = Field(
        None, description="Prediction context for the advisor"
    )
    history: Optional[List[Dict[str, str]]] = Field(
        None, description="Conversation history (list of {role, content} dicts)"
    )


class AdvisorResponse(BaseModel):
    """Response schema for AI advisor endpoint."""

    reply: str
    suggestions: List[str] = []


# --- Advanced AI/ML Schemas ---


class ExplainRequest(BaseModel):
    """Request schema for SHAP explainability endpoint."""

    scores: Dict[str, Any] = Field(
        ..., description="Student scores as subject -> semester -> score mapping"
    )
    school_ranking: int = Field(..., ge=1, description="Student ranking in school")
    total_students: int = Field(..., ge=1, description="Total students in school")
    school_accreditation: str = Field(
        ..., description="School accreditation: A, B, or C"
    )
    target_program_id: str = Field(..., description="Target program name or ID")
    jurusan: Optional[str] = Field(None, description="Student major/track")


class FeatureContribution(BaseModel):
    """A single feature's contribution to the prediction."""

    feature: str = Field(..., description="Feature name")
    value: float = Field(..., description="Feature input value")
    contribution: float = Field(..., description="SHAP contribution value")
    description: str = Field(..., description="Human-readable explanation in Indonesian")


class ExplainResponse(BaseModel):
    """Response schema for SHAP explainability endpoint."""

    success: bool = True
    shap_values: List[FeatureContribution] = Field(
        ..., description="Per-feature SHAP contributions sorted by absolute impact"
    )
    base_value: float = Field(..., description="Model base prediction value")
    prediction: float = Field(..., description="Final predicted probability (0-1)")
    explanation_text: str = Field(
        ..., description="Summary explanation in Indonesian"
    )


class BatchPredictionRequest(BaseModel):
    """Request schema for batch prediction endpoint."""

    students: List[PredictionRequest] = Field(
        ..., description="List of student prediction requests (max 50)"
    )

    @field_validator("students")
    @classmethod
    def validate_students_count(cls, v):
        if len(v) > 50:
            raise ValueError("Maksimal 50 siswa per batch request")
        if len(v) == 0:
            raise ValueError("Minimal 1 siswa per batch request")
        return v


class BatchPredictionSummary(BaseModel):
    """Summary statistics for batch prediction."""

    count: int
    avg_probability: float
    highest: float
    lowest: float


class BatchPredictionResponse(BaseModel):
    """Response schema for batch prediction endpoint."""

    success: bool = True
    results: List[PredictionResponse]
    summary: BatchPredictionSummary


class WhatIfRequest(BaseModel):
    """Request schema for what-if analysis endpoint."""

    scores: Dict[str, Any] = Field(
        ..., description="Student scores as subject -> semester -> score mapping"
    )
    school_ranking: int = Field(..., ge=1, description="Student ranking in school")
    total_students: int = Field(..., ge=1, description="Total students in school")
    school_accreditation: str = Field(
        ..., description="School accreditation: A, B, or C"
    )
    target_program_id: str = Field(..., description="Target program name or ID")
    jurusan: Optional[str] = Field(None, description="Student major/track")
    variable_to_change: str = Field(
        ...,
        description="Variable to modify: avg_score, school_ranking, school_accreditation, or target_program_id",
    )
    new_value: str = Field(
        ...,
        description="New value for the variable (string, will be cast appropriately)",
    )

    @field_validator("variable_to_change")
    @classmethod
    def validate_variable_name(cls, v):
        allowed = ["avg_score", "school_ranking", "school_accreditation", "target_program_id"]
        if v not in allowed:
            raise ValueError(
                f"variable_to_change harus salah satu dari: {', '.join(allowed)}"
            )
        return v


class WhatIfResponse(BaseModel):
    """Response schema for what-if analysis endpoint."""

    success: bool = True
    original_probability: float = Field(
        ..., description="Original prediction probability (0-100)"
    )
    new_probability: float = Field(
        ..., description="New prediction probability after change (0-100)"
    )
    change: float = Field(
        ..., description="Delta between new and original probability"
    )
    variable_changed: str = Field(..., description="Name of variable that was changed")
    insight: str = Field(
        ..., description="Insight message in Indonesian explaining the impact"
    )
