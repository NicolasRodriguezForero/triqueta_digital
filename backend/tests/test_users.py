"""
Tests for user profile endpoints.
"""
import pytest
from httpx import AsyncClient


async def _create_and_login_user(client: AsyncClient, user_data: dict) -> dict:
    """Helper to create a user and return tokens."""
    await client.post("/api/v1/auth/register", json=user_data)
    login_response = await client.post("/api/v1/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    return login_response.json()


@pytest.mark.asyncio
async def test_get_user_profile(client: AsyncClient, sample_user_data):
    """Test getting user profile."""
    tokens = await _create_and_login_user(client, sample_user_data)
    
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert "perfil" in data
    assert data["perfil"] is not None


@pytest.mark.asyncio
async def test_get_user_profile_unauthorized(client: AsyncClient):
    """Test getting profile without authentication fails."""
    response = await client.get("/api/v1/users/me")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_user_profile(client: AsyncClient, sample_user_data):
    """Test updating user profile."""
    tokens = await _create_and_login_user(client, sample_user_data)
    
    # Update profile
    profile_update = {
        "nombre_completo": "Updated Name",
        "telefono": "3001234567",
        "biografia": "This is my bio",
        "localidad_preferida": "Chapinero"
    }
    
    response = await client.put(
        "/api/v1/users/me/profile",
        json=profile_update,
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_completo"] == profile_update["nombre_completo"]
    assert data["telefono"] == profile_update["telefono"]
    assert data["biografia"] == profile_update["biografia"]
    assert data["localidad_preferida"] == profile_update["localidad_preferida"]


@pytest.mark.asyncio
async def test_update_profile_etiquetas_interes(client: AsyncClient, sample_user_data):
    """Test updating user interest tags."""
    tokens = await _create_and_login_user(client, sample_user_data)
    
    # Update with interest tags
    profile_update = {
        "etiquetas_interes": ["arte", "música", "deportes", "cultura"]
    }
    
    response = await client.put(
        "/api/v1/users/me/profile",
        json=profile_update,
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["etiquetas_interes"]) == 4
    assert "arte" in data["etiquetas_interes"]
    assert "música" in data["etiquetas_interes"]


@pytest.mark.asyncio
async def test_update_profile_disponibilidad_nivel(client: AsyncClient, sample_user_data):
    """Test updating availability and activity level."""
    tokens = await _create_and_login_user(client, sample_user_data)
    
    profile_update = {
        "disponibilidad_horaria": "fin_de_semana",
        "nivel_actividad": "alto"
    }
    
    response = await client.put(
        "/api/v1/users/me/profile",
        json=profile_update,
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["disponibilidad_horaria"] == "fin_de_semana"
    assert data["nivel_actividad"] == "alto"


@pytest.mark.asyncio
async def test_update_profile_partial(client: AsyncClient, sample_user_data):
    """Test partial profile update (only some fields)."""
    tokens = await _create_and_login_user(client, sample_user_data)
    
    # Update only phone
    profile_update = {
        "telefono": "3009876543"
    }
    
    response = await client.put(
        "/api/v1/users/me/profile",
        json=profile_update,
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["telefono"] == "3009876543"
    # Other fields should remain unchanged
    assert data["nombre_completo"] == sample_user_data["nombre_completo"]


@pytest.mark.asyncio
async def test_delete_user_account(client: AsyncClient, sample_user_data):
    """Test deleting user account (soft delete)."""
    tokens = await _create_and_login_user(client, sample_user_data)
    
    # Delete account
    response = await client.delete(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    
    assert response.status_code == 204
    
    # Try to login with deleted account
    login_response = await client.post("/api/v1/auth/login", json={
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    })
    
    # Should fail because account is inactive
    assert login_response.status_code == 403


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, sample_user_data):
    """Test getting user by ID."""
    tokens = await _create_and_login_user(client, sample_user_data)
    
    # Get own profile first to get ID
    profile_response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    user_id = profile_response.json()["id"]
    
    # Get user by ID
    response = await client.get(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == sample_user_data["email"]


@pytest.mark.asyncio
async def test_update_profile_unauthorized(client: AsyncClient):
    """Test updating profile without authentication fails."""
    profile_update = {
        "nombre_completo": "Hacker"
    }
    
    response = await client.put(
        "/api/v1/users/me/profile",
        json=profile_update
    )
    
    assert response.status_code == 401
