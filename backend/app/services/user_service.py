"""
User service for profile management.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.user import Usuario, PerfilUsuario
from app.schemas.user import PerfilUsuarioUpdate, UsuarioUpdate
from app.core.security import get_password_hash


async def get_user_profile(
    db: AsyncSession,
    user_id: int
) -> Usuario:
    """
    Get user with profile data.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        User instance with profile
        
    Raises:
        HTTPException: If user not found
    """
    stmt = select(Usuario).options(selectinload(Usuario.perfil)).where(Usuario.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


async def update_user_profile(
    db: AsyncSession,
    user_id: int,
    profile_data: PerfilUsuarioUpdate
) -> PerfilUsuario:
    """
    Update user profile.
    
    Args:
        db: Database session
        user_id: User ID
        profile_data: Profile update data
        
    Returns:
        Updated profile instance
        
    Raises:
        HTTPException: If user not found
    """
    # Get user's profile
    stmt = select(PerfilUsuario).where(PerfilUsuario.usuario_id == user_id)
    result = await db.execute(stmt)
    perfil = result.scalar_one_or_none()
    
    if not perfil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    # Update fields if provided
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(perfil, field, value)
    
    await db.commit()
    await db.refresh(perfil)
    
    return perfil


async def update_user(
    db: AsyncSession,
    user_id: int,
    user_data: UsuarioUpdate
) -> Usuario:
    """
    Update user account information.
    
    Args:
        db: Database session
        user_id: User ID
        user_data: User update data
        
    Returns:
        Updated user instance
        
    Raises:
        HTTPException: If user not found or email already exists
    """
    # Get user with profile
    stmt = select(Usuario).options(selectinload(Usuario.perfil)).where(Usuario.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if email is being updated and if it already exists
    if user_data.email and user_data.email != user.email:
        stmt = select(Usuario).where(Usuario.email == user_data.email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update fields if provided
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return user


async def delete_user(
    db: AsyncSession,
    user_id: int
) -> bool:
    """
    Delete user account (soft delete by setting is_active=False).
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        True if successful
        
    Raises:
        HTTPException: If user not found
    """
    stmt = select(Usuario).options(selectinload(Usuario.perfil)).where(Usuario.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    await db.commit()
    
    return True
