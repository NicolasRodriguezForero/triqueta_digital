"""
Dependency injection functions for FastAPI.
"""
from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_session
from app.models.user import Usuario


# OAuth2 scheme for token authentication (uses form endpoint for Swagger UI compatibility)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/form")

# OAuth2 scheme for optional authentication (does not raise error if no token)
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/form", auto_error=False)


async def get_db() -> AsyncSession:
    """
    Dependency to get async database session.
    
    Yields:
        AsyncSession: Database session
    """
    async for session in get_session():
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Usuario:
    """
    Dependency to get current authenticated user from JWT token.
    
    Args:
        token: JWT access token
        db: Database session
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    from app.services.auth_service import get_user_by_id
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Dependency to get current active user.
    
    Args:
        current_user: Current user from token
        
    Returns:
        Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_admin_user(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """
    Dependency to get current admin user.
    
    Args:
        current_user: Current active user
        
    Returns:
        Current admin user
        
    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: AsyncSession = Depends(get_db)
) -> Optional[Usuario]:
    """
    Dependency to get current user if authenticated, None otherwise.
    
    Unlike get_current_user, this does not raise an exception if no token
    is provided or if the token is invalid. Useful for endpoints that
    work both with and without authentication.
    
    Args:
        token: Optional JWT access token
        db: Database session
        
    Returns:
        Current user object if authenticated, None otherwise
    """
    if not token:
        return None
    
    try:
        from app.services.auth_service import get_user_by_id
        
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        
        user = await get_user_by_id(db, int(user_id))
        return user
    except JWTError:
        return None
