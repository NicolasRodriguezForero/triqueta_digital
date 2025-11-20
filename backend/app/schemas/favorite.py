"""
Pydantic schemas for favorites.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class FavoritoCreate(BaseModel):
    """
    Schema for creating a favorite.
    
    Attributes:
        actividad_id: UUID of the activity to favorite
    """
    actividad_id: UUID = Field(..., description="UUID of the activity to add to favorites")


class FavoritoResponse(BaseModel):
    """
    Schema for favorite response.
    
    Attributes:
        id: Favorite UUID
        usuario_id: User ID
        actividad_id: Activity UUID
        fecha_guardado: When the favorite was created
    """
    id: UUID
    usuario_id: int
    actividad_id: UUID
    fecha_guardado: datetime
    
    class Config:
        from_attributes = True


class FavoritoWithActivity(BaseModel):
    """
    Schema for favorite with full activity details.
    
    Includes the complete activity object.
    """
    id: UUID
    usuario_id: int
    actividad_id: UUID
    fecha_guardado: datetime
    actividad: Optional[dict] = None  # Will be populated with full Actividad schema
    
    class Config:
        from_attributes = True


class FavoritoList(BaseModel):
    """
    Schema for paginated favorite list.
    
    Attributes:
        items: List of favorites with activities
        total: Total count of favorites
        page: Current page
        page_size: Items per page
        total_pages: Total number of pages
    """
    items: list[FavoritoWithActivity]
    total: int
    page: int
    page_size: int
    total_pages: int


class IsFavoriteResponse(BaseModel):
    """
    Schema for checking if activity is favorited.
    
    Attributes:
        is_favorite: Whether the activity is in user's favorites
        favorito_id: UUID of the favorite if it exists
    """
    is_favorite: bool
    favorito_id: Optional[UUID] = None
