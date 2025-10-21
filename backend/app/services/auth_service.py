"""
Authentication service for user registration, login, and token management.
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.core.config import settings
from app.models.user import Usuario, PerfilUsuario, RefreshToken
from app.schemas.auth import UserRegister, UserLogin, Token
from app.schemas.user import PerfilUsuarioCreate


async def register_user(
    db: AsyncSession,
    user_data: UserRegister
) -> Usuario:
    """
    Register a new user with optional profile data.
    
    Args:
        db: Database session
        user_data: User registration data
        
    Returns:
        Created user instance
        
    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    stmt = select(Usuario).where(Usuario.email == user_data.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    hashed_password = get_password_hash(user_data.password)
    db_user = Usuario(
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False
    )
    db.add(db_user)
    await db.flush()
    
    # Create profile
    db_perfil = PerfilUsuario(
        usuario_id=db_user.id,
        nombre_completo=user_data.nombre_completo,
        etiquetas_interes=[]
    )
    db.add(db_perfil)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


async def login_user(
    db: AsyncSession,
    credentials: UserLogin
) -> Token:
    """
    Authenticate user and generate tokens.
    
    Args:
        db: Database session
        credentials: User login credentials
        
    Returns:
        JWT tokens (access and refresh)
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Get user by email
    stmt = select(Usuario).where(Usuario.email == credentials.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Generate tokens
    access_token = create_access_token(subject=str(user.id))
    refresh_token_str = create_refresh_token(subject=str(user.id))
    
    # Store refresh token in database
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db_refresh_token = RefreshToken(
        usuario_id=user.id,
        token=refresh_token_str,
        expires_at=expires_at,
        revoked=False
    )
    db.add(db_refresh_token)
    await db.commit()
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token_str,
        token_type="bearer"
    )


async def refresh_access_token(
    db: AsyncSession,
    refresh_token: str
) -> Token:
    """
    Generate new access token using refresh token.
    
    Args:
        db: Database session
        refresh_token: JWT refresh token
        
    Returns:
        New JWT tokens
        
    Raises:
        HTTPException: If refresh token is invalid or revoked
    """
    # Verify refresh token exists and is not revoked
    stmt = select(RefreshToken).where(
        RefreshToken.token == refresh_token,
        RefreshToken.revoked == False
    )
    result = await db.execute(stmt)
    db_token = result.scalar_one_or_none()
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Check if token is expired
    if db_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    
    # Get user
    stmt = select(Usuario).where(Usuario.id == db_token.usuario_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Generate new tokens
    new_access_token = create_access_token(subject=str(user.id))
    new_refresh_token = create_refresh_token(subject=str(user.id))
    
    # Revoke old refresh token
    db_token.revoked = True
    
    # Store new refresh token
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    new_db_token = RefreshToken(
        usuario_id=user.id,
        token=new_refresh_token,
        expires_at=expires_at,
        revoked=False
    )
    db.add(new_db_token)
    await db.commit()
    
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


async def logout_user(
    db: AsyncSession,
    refresh_token: str
) -> bool:
    """
    Logout user by revoking refresh token.
    
    Args:
        db: Database session
        refresh_token: JWT refresh token to revoke
        
    Returns:
        True if successful
    """
    stmt = select(RefreshToken).where(RefreshToken.token == refresh_token)
    result = await db.execute(stmt)
    db_token = result.scalar_one_or_none()
    
    if db_token:
        db_token.revoked = True
        await db.commit()
    
    return True


async def get_user_by_email(
    db: AsyncSession,
    email: str
) -> Optional[Usuario]:
    """
    Get user by email address.
    
    Args:
        db: Database session
        email: User email
        
    Returns:
        User instance or None
    """
    stmt = select(Usuario).where(Usuario.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_id(
    db: AsyncSession,
    user_id: int
) -> Optional[Usuario]:
    """
    Get user by ID.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        User instance or None
    """
    stmt = select(Usuario).where(Usuario.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
