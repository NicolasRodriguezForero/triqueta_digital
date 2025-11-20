"""
API endpoints for personalized recommendations.

Implements requirements RF-014 to RF-015 from SRS.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import Usuario
from app.schemas.recommendation import RecommendationList, RecommendationQuery
from app.services.recommendation_service import recommendation_service

router = APIRouter()


@router.get(
    "",
    response_model=RecommendationList,
    summary="Get personalized recommendations",
    description="Get personalized activity recommendations based on user profile and preferences (RF-014, RF-015)"
)
async def get_recommendations(
    limit: int = Query(default=10, ge=1, le=50, description="Number of recommendations to return"),
    tipo: str = Query(default=None, description="Filter by activity type"),
    localidad: str = Query(default=None, description="Filter by locality"),
    exclude_favorited: bool = Query(default=False, description="Exclude already favorited activities"),
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Get personalized activity recommendations.
    
    The recommendation algorithm uses a hybrid approach:
    1. **Popularity score**: Base score from community engagement (favorites + views)
    2. **Tag matching**: Bonus points for activities matching user's interests (+10 per tag)
    3. **Location matching**: Bonus for activities in preferred locality (+5 points)
    4. **Activity level matching**: Bonus for matching physical activity level (+3 points)
    
    Each recommendation includes:
    - Full activity details
    - Recommendation score (0-100)
    - Explanation of why it was recommended
    - Whether user has already favorited it
    
    Query parameters:
    - **limit**: Number of recommendations (default: 10, max: 50)
    - **tipo**: Filter by activity type (optional)
    - **localidad**: Filter by locality (optional)
    - **exclude_favorited**: Exclude activities user has already favorited (default: false)
    
    Responses are cached for 1 hour per user. Cache is invalidated when:
    - User adds/removes favorites
    - User updates their profile
    
    Returns:
    - List of recommendations sorted by score (highest first)
    - Total number of recommendations
    - Flag indicating if user profile is complete for better recommendations
    """
    query_params = RecommendationQuery(
        limit=limit,
        tipo=tipo,
        localidad=localidad,
        exclude_favorited=exclude_favorited
    )
    
    recommendations = await recommendation_service.get_recommendations(
        db=db,
        usuario_id=current_user.id,
        query_params=query_params
    )
    
    return recommendations
