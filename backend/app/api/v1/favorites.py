"""
API endpoints for favorites management.

Implements requirements RF-011 to RF-013 from SRS.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import Usuario
from app.schemas.favorite import (
    FavoritoCreate,
    FavoritoResponse,
    FavoritoList,
    IsFavoriteResponse
)
from app.services.favorite_service import FavoriteService
from app.services.recommendation_service import recommendation_service

router = APIRouter()


@router.post(
    "",
    response_model=FavoritoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add activity to favorites",
    description="Add an activity to the authenticated user's favorites list (RF-011)"
)
async def add_favorite(
    favorito_data: FavoritoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Add activity to user's favorites.
    
    - **actividad_id**: UUID of the activity to favorite
    
    Returns the created favorite.
    Raises 400 if activity already in favorites or not found.
    """
    try:
        favorito = await FavoriteService.add_favorite(
            db=db,
            usuario_id=current_user.id,
            favorito_data=favorito_data
        )
        
        # Invalidate recommendation cache
        await recommendation_service.invalidate_cache(current_user.id)
        
        return favorito
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "",
    response_model=FavoritoList,
    summary="List user favorites",
    description="Get paginated list of user's favorite activities with optional filters (RF-013)"
)
async def list_favorites(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    tipo: str = Query(default=None, description="Filter by activity type"),
    localidad: str = Query(default=None, description="Filter by locality"),
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Get user's favorite activities with pagination and filters.
    
    Query parameters:
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **tipo**: Filter by activity type (optional)
    - **localidad**: Filter by locality (optional)
    
    Returns paginated list of favorites with full activity details.
    """
    favoritos = await FavoriteService.get_user_favorites(
        db=db,
        usuario_id=current_user.id,
        page=page,
        page_size=page_size,
        tipo=tipo,
        localidad=localidad
    )
    
    return favoritos


@router.delete(
    "/{actividad_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove activity from favorites",
    description="Remove an activity from user's favorites list (RF-012)"
)
async def remove_favorite(
    actividad_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Remove activity from user's favorites.
    
    - **actividad_id**: UUID of the activity to remove from favorites
    
    Returns 204 No Content on success.
    Raises 404 if favorite not found.
    """
    removed = await FavoriteService.remove_favorite(
        db=db,
        usuario_id=current_user.id,
        actividad_id=actividad_id
    )
    
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    # Invalidate recommendation cache
    await recommendation_service.invalidate_cache(current_user.id)
    
    return None


@router.get(
    "/check/{actividad_id}",
    response_model=IsFavoriteResponse,
    summary="Check if activity is favorited",
    description="Check if a specific activity is in user's favorites"
)
async def check_is_favorite(
    actividad_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Check if activity is in user's favorites.
    
    - **actividad_id**: UUID of the activity to check
    
    Returns whether the activity is favorited and the favorite ID if it exists.
    """
    is_favorite, favorito_id = await FavoriteService.is_favorite(
        db=db,
        usuario_id=current_user.id,
        actividad_id=actividad_id
    )
    
    return IsFavoriteResponse(
        is_favorite=is_favorite,
        favorito_id=favorito_id
    )


@router.get(
    "/count",
    response_model=dict,
    summary="Get favorite count",
    description="Get total count of user's favorites"
)
async def get_favorite_count(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Get total count of user's favorites.
    
    Returns simple count object.
    """
    count = await FavoriteService.get_favorite_count(
        db=db,
        usuario_id=current_user.id
    )
    
    return {"count": count}
