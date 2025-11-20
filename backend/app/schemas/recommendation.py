"""
Pydantic schemas for recommendations.
"""
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class RecommendationExplanation(BaseModel):
    """
    Schema for recommendation explanation.
    
    Provides context on why an activity was recommended.
    
    Attributes:
        reason: Main reason for recommendation
        details: Additional details (e.g., "3 matching tags", "En tu localidad preferida")
    """
    reason: str = Field(..., description="Main reason category (e.g., 'popular', 'tags', 'location')")
    details: str = Field(..., description="Human-readable explanation details")


class RecommendationResponse(BaseModel):
    """
    Schema for a single recommendation.
    
    Attributes:
        actividad: Full activity object (using dict for now, can be typed later)
        score: Recommendation score (0-100)
        explanation: Why this was recommended
        is_favorite: Whether user has already favorited this
    """
    actividad: dict  # Will contain full Actividad schema data
    score: float = Field(..., ge=0, le=100, description="Recommendation score from 0 to 100")
    explanation: RecommendationExplanation
    is_favorite: bool = Field(default=False, description="Whether activity is in user's favorites")
    
    class Config:
        from_attributes = True


class RecommendationList(BaseModel):
    """
    Schema for list of recommendations.
    
    Attributes:
        items: List of recommended activities
        total: Total number of recommendations generated
        user_profile_complete: Whether user has completed profile for better recommendations
    """
    items: list[RecommendationResponse]
    total: int
    user_profile_complete: bool = Field(
        description="Whether user profile has enough data for personalized recommendations"
    )


class RecommendationQuery(BaseModel):
    """
    Schema for recommendation query parameters.
    
    Attributes:
        limit: Maximum number of recommendations to return
        tipo: Filter by activity type
        localidad: Filter by locality
        exclude_favorited: Whether to exclude already favorited activities
    """
    limit: int = Field(default=10, ge=1, le=50, description="Number of recommendations")
    tipo: Optional[str] = Field(default=None, description="Filter by activity type")
    localidad: Optional[str] = Field(default=None, description="Filter by locality")
    exclude_favorited: bool = Field(default=False, description="Exclude already favorited activities")
