"""
Tests for authentication endpoints.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, sample_user_data):
    """Test successful user registration."""
    response = await client.post("/api/v1/auth/register", json=sample_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert "id" in data
    assert data["is_active"] is True
    assert data["is_admin"] is False
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, sample_user_data):
    """Test registration with duplicate email fails."""
    # Register first user
    await client.post("/api/v1/auth/register", json=sample_user_data)
    
    # Try to register again with same email
    response = await client.post("/api/v1/auth/register", json=sample_user_data)
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    """Test registration with weak password fails."""
    weak_data = {
        "email": "weak@example.com",
        "password": "123",  # Too short, no letters
        "nombre_completo": "Weak User"
    }
    
    response = await client.post("/api/v1/auth/register", json=weak_data)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, sample_user_data):
    """Test successful login."""
    # Register user first
    await client.post("/api/v1/auth/register", json=sample_user_data)
    
    # Login
    login_data = {
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, sample_user_data):
    """Test login with wrong password fails."""
    # Register user first
    await client.post("/api/v1/auth/register", json=sample_user_data)
    
    # Try to login with wrong password
    login_data = {
        "email": sample_user_data["email"],
        "password": "WrongPassword123"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Test login with non-existent user fails."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "SomePassword123"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, sample_user_data):
    """Test getting current user information."""
    # Register and login
    await client.post("/api/v1/auth/register", json=sample_user_data)
    login_response = await client.post("/api/v1/auth/login", json={
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    })
    access_token = login_response.json()["access_token"]
    
    # Get current user
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_current_user_without_token(client: AsyncClient):
    """Test getting current user without token fails."""
    response = await client.get("/api/v1/auth/me")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient, sample_user_data):
    """Test refreshing access token."""
    # Register and login
    await client.post("/api/v1/auth/register", json=sample_user_data)
    login_response = await client.post("/api/v1/auth/login", json={
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    })
    refresh_token = login_response.json()["refresh_token"]
    
    # Refresh token
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    # New tokens should be different from old ones
    assert data["access_token"] != login_response.json()["access_token"]


@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient, sample_user_data):
    """Test logout revokes refresh token."""
    # Register and login
    await client.post("/api/v1/auth/register", json=sample_user_data)
    login_response = await client.post("/api/v1/auth/login", json={
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    })
    tokens = login_response.json()
    
    # Logout
    response = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": tokens["refresh_token"]},
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    
    assert response.status_code == 204
    
    # Try to use the revoked refresh token
    refresh_response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]}
    )
    
    assert refresh_response.status_code == 401


@pytest.mark.asyncio
async def test_oauth2_password_flow(client: AsyncClient, sample_user_data):
    """Test OAuth2 password flow (form-based login)."""
    # Register user first
    await client.post("/api/v1/auth/register", json=sample_user_data)
    
    # Login using OAuth2 form
    form_data = {
        "username": sample_user_data["email"],
        "password": sample_user_data["password"]
    }
    response = await client.post(
        "/api/v1/auth/login/form",
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
