"""
Authentication endpoints for registration, login, and token management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.schemas.auth import UserRegister, UserLogin, Token, TokenRefresh
from app.schemas.user import UsuarioResponse
from app.services import auth_service
from app.models.user import Usuario

router = APIRouter()


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    
    - **email**: Valid email address (must be unique)
    - **password**: Password (min 8 characters, must contain letters and numbers)
    - **nombre_completo**: Optional full name
    """
    user = await auth_service.register_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password to get JWT tokens.
    
    Returns access_token and refresh_token.
    """
    return await auth_service.login_user(db, credentials)


@router.post("/login/form", response_model=Token)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Login with OAuth2 password flow (for compatibility).
    
    Uses username as email field.
    """
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    return await auth_service.login_user(db, credentials)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """
    Get new access token using refresh token.
    
    - **refresh_token**: Valid JWT refresh token
    """
    return await auth_service.refresh_access_token(db, token_data.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Logout by revoking refresh token.
    
    Requires authentication.
    """
    await auth_service.logout_user(db, token_data.refresh_token)
    return None


@router.get("/me", response_model=UsuarioResponse)
async def get_current_user_info(
    current_user: Usuario = Depends(get_current_user)
):
    """
    Get current authenticated user information.
    
    Requires authentication.
    """
    return current_user
