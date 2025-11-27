"""
User endpoints for profile management.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user, get_current_active_user
from app.schemas.user import (
    UsuarioResponse,
    UsuarioWithProfile,
    PerfilUsuarioUpdate,
    PerfilUsuarioResponse
)
from app.services import user_service
from app.services.recommendation_service import recommendation_service
from app.models.user import Usuario

router = APIRouter()


@router.get("/me", response_model=UsuarioWithProfile)
async def get_my_profile(
    current_user: Usuario = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user profile with all information.
    
    Requires authentication.
    """
    return await user_service.get_user_profile(db, current_user.id)


@router.put("/me/profile", response_model=PerfilUsuarioResponse)
async def update_my_profile(
    profile_data: PerfilUsuarioUpdate,
    current_user: Usuario = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user profile.
    
    - **nombre_completo**: Full name
    - **telefono**: Phone number
    - **biografia**: Biography text
    - **etiquetas_interes**: Array of interest tags (e.g., ["arte", "música", "deportes"])
    - **localidad_preferida**: Preferred locality (Chapinero, Santa Fe, La Candelaria)
    - **disponibilidad_horaria**: Preferred time (mañana, tarde, noche, fin_de_semana)
    - **nivel_actividad**: Activity level (bajo, medio, alto)
    
    All fields are optional.
    """
    result = await user_service.update_user_profile(db, current_user.id, profile_data)
    
    # Invalidate recommendation cache since profile affects personalization
    await recommendation_service.invalidate_cache(current_user.id)
    
    return result


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    current_user: Usuario = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete current user account (soft delete).
    
    Sets is_active=False instead of removing from database.
    """
    await user_service.delete_user(db, current_user.id)
    return None


@router.get("/{user_id}", response_model=UsuarioResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Get user by ID (public information only).
    
    Requires authentication.
    """
    return await user_service.get_user_profile(db, user_id)
