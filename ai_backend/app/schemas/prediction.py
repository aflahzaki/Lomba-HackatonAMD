"""Pydantic schemas for request/response models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


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
