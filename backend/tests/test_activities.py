"""
Tests for activity endpoints (RF-006 to RF-010).
"""
import pytest
import pytest_asyncio
from datetime import datetime, timedelta
from httpx import AsyncClient
from uuid import UUID


@pytest.fixture
def sample_activity_data():
    """Sample activity data for tests."""
    return {
        "titulo": "Taller de Arte Urbano",
        "descripcion": "Aprende técnicas de arte urbano con artistas locales en un taller práctico",
        "tipo": "cultura",
        "fecha_inicio": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "ubicacion_direccion": "Calle 53 #10-15, Chapinero",
        "ubicacion_lat": "4.65389",
        "ubicacion_lng": "-74.06141",
        "localidad": "Chapinero",
        "precio": "0",
        "es_gratis": True,
        "etiquetas": ["arte", "urbano", "taller", "cultura"],
    }


@pytest_asyncio.fixture
async def admin_token(db_session):
    """Create admin user and return access token."""
    from app.models.user import Usuario
    from app.core.security import get_password_hash, create_access_token
    
    # Create admin user directly in DB
    admin = Usuario(
        email="admin@example.com",
        hashed_password=get_password_hash("Admin1234"),
        is_active=True,
        is_admin=True
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    
    # Generate token directly (bypass HTTP to avoid Redis/event loop issues)
    access_token = create_access_token(subject=str(admin.id))
    return access_token


@pytest_asyncio.fixture
async def regular_user_token(client: AsyncClient):
    """Create regular user and return access token."""
    user_data = {
        "email": "user@example.com",
        "password": "User1234",
        "nombre_completo": "Regular User"
    }
    await client.post("/api/v1/auth/register", json=user_data)
    
    login_response = await client.post("/api/v1/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    
    return login_response.json()["access_token"]


# Test RF-009: Create Activity (Admin only)
@pytest.mark.asyncio
async def test_create_activity_success(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test successful activity creation by admin."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.post(
        "/api/v1/actividades",
        json=sample_activity_data,
        headers=headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == sample_activity_data["titulo"]
    assert data["tipo"] == sample_activity_data["tipo"]
    assert data["localidad"] == sample_activity_data["localidad"]
    assert "id" in data
    assert data["estado"] == "activa"


@pytest.mark.asyncio
async def test_create_activity_unauthorized(client: AsyncClient, sample_activity_data):
    """Test that activity creation requires authentication."""
    response = await client.post("/api/v1/actividades", json=sample_activity_data)
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_activity_invalid_tipo(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test activity creation with invalid tipo fails validation."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    invalid_data = {**sample_activity_data, "tipo": "invalido"}
    
    response = await client.post(
        "/api/v1/actividades",
        json=invalid_data,
        headers=headers
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_activity_invalid_localidad(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test activity creation with invalid localidad fails validation."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    invalid_data = {**sample_activity_data, "localidad": "Bogotá"}  # Not in allowed list
    
    response = await client.post(
        "/api/v1/actividades",
        json=invalid_data,
        headers=headers
    )
    
    assert response.status_code == 422


# Test RF-006: List Activities
@pytest.mark.asyncio
async def test_list_activities_empty(client: AsyncClient):
    """Test listing activities when database is empty."""
    response = await client.get("/api/v1/actividades")
    
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == []
    assert data["pagination"]["total"] == 0


@pytest.mark.asyncio
async def test_list_activities_with_data(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test listing activities returns created activities."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create 3 activities
    for i in range(3):
        activity_data = {
            **sample_activity_data,
            "titulo": f"Actividad {i+1}"
        }
        await client.post("/api/v1/actividades", json=activity_data, headers=headers)
    
    # List activities
    response = await client.get("/api/v1/actividades")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 3
    assert data["pagination"]["total"] == 3
    assert data["pagination"]["page"] == 1


@pytest.mark.asyncio
async def test_list_activities_pagination(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test activity list pagination."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create 5 activities
    for i in range(5):
        activity_data = {
            **sample_activity_data,
            "titulo": f"Actividad {i+1}"
        }
        await client.post("/api/v1/actividades", json=activity_data, headers=headers)
    
    # Get page 1 with page_size=2
    response = await client.get("/api/v1/actividades?page=1&page_size=2")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["pagination"]["total"] == 5
    assert data["pagination"]["total_pages"] == 3


@pytest.mark.asyncio
async def test_list_activities_filter_by_tipo(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test filtering activities by tipo."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create cultura activity
    await client.post("/api/v1/actividades", json=sample_activity_data, headers=headers)
    
    # Create deporte activity
    deporte_data = {**sample_activity_data, "titulo": "Partido de Fútbol", "tipo": "deporte"}
    await client.post("/api/v1/actividades", json=deporte_data, headers=headers)
    
    # Filter by tipo=cultura
    response = await client.get("/api/v1/actividades?tipo=cultura")
    
    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["total"] == 1
    assert data["data"][0]["tipo"] == "cultura"


@pytest.mark.asyncio
async def test_list_activities_filter_by_localidad(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test filtering activities by localidad."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create Chapinero activity
    await client.post("/api/v1/actividades", json=sample_activity_data, headers=headers)
    
    # Create Santa Fe activity
    santa_fe_data = {
        **sample_activity_data,
        "titulo": "Concierto en Santa Fe",
        "localidad": "Santa Fe",
        "ubicacion_direccion": "Carrera 5 #12-30, Santa Fe"
    }
    await client.post("/api/v1/actividades", json=santa_fe_data, headers=headers)
    
    # Filter by localidad=Chapinero
    response = await client.get("/api/v1/actividades?localidad=Chapinero")
    
    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["total"] == 1
    assert data["data"][0]["localidad"] == "Chapinero"


@pytest.mark.asyncio
async def test_list_activities_filter_by_es_gratis(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test filtering activities by es_gratis."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create free activity
    await client.post("/api/v1/actividades", json=sample_activity_data, headers=headers)
    
    # Create paid activity
    paid_data = {
        **sample_activity_data,
        "titulo": "Taller Privado",
        "precio": "50000",
        "es_gratis": False
    }
    await client.post("/api/v1/actividades", json=paid_data, headers=headers)
    
    # Filter by es_gratis=true
    response = await client.get("/api/v1/actividades?es_gratis=true")
    
    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["total"] == 1
    assert data["data"][0]["es_gratis"] is True


# Test RF-008: Search Activities
@pytest.mark.asyncio
async def test_search_activities_by_titulo(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test searching activities by titulo."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create activities
    await client.post("/api/v1/actividades", json=sample_activity_data, headers=headers)
    
    other_data = {
        **sample_activity_data, 
        "titulo": "Concierto de Rock",
        "descripcion": "Disfruta de un gran concierto de rock en vivo con bandas locales",
        "etiquetas": ["musica", "rock", "concierto"]  # Different tags without "arte"
    }
    await client.post("/api/v1/actividades", json=other_data, headers=headers)
    
    # Search for "Arte"
    response = await client.get("/api/v1/actividades?q=Arte")
    
    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["total"] == 1
    assert "arte" in data["data"][0]["titulo"].lower()


@pytest.mark.asyncio
async def test_search_activities_by_etiquetas(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test searching activities by etiquetas."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    await client.post("/api/v1/actividades", json=sample_activity_data, headers=headers)
    
    # Search for "taller"
    response = await client.get("/api/v1/actividades?q=taller")
    
    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["total"] >= 1


# Test RF-007: Get Activity Detail
@pytest.mark.asyncio
async def test_get_activity_detail(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test getting activity detail."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create activity
    create_response = await client.post(
        "/api/v1/actividades",
        json=sample_activity_data,
        headers=headers
    )
    activity_id = create_response.json()["id"]
    
    # Get detail
    response = await client.get(f"/api/v1/actividades/{activity_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == activity_id
    assert data["titulo"] == sample_activity_data["titulo"]
    assert "descripcion" in data
    assert "popularidad_vistas" in data


@pytest.mark.asyncio
async def test_get_activity_detail_not_found(client: AsyncClient):
    """Test getting non-existent activity returns 404."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/api/v1/actividades/{fake_uuid}")
    
    assert response.status_code == 404


# Test RF-009: Update Activity
@pytest.mark.asyncio
async def test_update_activity_success(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test updating activity by admin."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create activity
    create_response = await client.post(
        "/api/v1/actividades",
        json=sample_activity_data,
        headers=headers
    )
    activity_id = create_response.json()["id"]
    
    # Update activity
    update_data = {"titulo": "Taller de Arte Urbano - Actualizado"}
    response = await client.put(
        f"/api/v1/actividades/{activity_id}",
        json=update_data,
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == update_data["titulo"]


@pytest.mark.asyncio
async def test_update_activity_unauthorized(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test that activity update requires authentication."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create activity as admin
    create_response = await client.post(
        "/api/v1/actividades",
        json=sample_activity_data,
        headers=headers
    )
    activity_id = create_response.json()["id"]
    
    # Try to update without auth
    update_data = {"titulo": "Nuevo Titulo"}
    response = await client.put(
        f"/api/v1/actividades/{activity_id}",
        json=update_data
    )
    
    assert response.status_code == 401


# Test RF-009: Delete Activity (Soft Delete)
@pytest.mark.asyncio
async def test_delete_activity_success(client: AsyncClient, admin_token: str, sample_activity_data):
    """Test deleting activity by admin."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create activity
    create_response = await client.post(
        "/api/v1/actividades",
        json=sample_activity_data,
        headers=headers
    )
    activity_id = create_response.json()["id"]
    
    # Delete activity
    response = await client.delete(
        f"/api/v1/actividades/{activity_id}",
        headers=headers
    )
    
    assert response.status_code == 204
    
    # Verify activity is not in public list
    list_response = await client.get("/api/v1/actividades")
    assert list_response.json()["pagination"]["total"] == 0


@pytest.mark.asyncio
async def test_delete_activity_not_found(client: AsyncClient, admin_token: str):
    """Test deleting non-existent activity returns 404."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    
    response = await client.delete(
        f"/api/v1/actividades/{fake_uuid}",
        headers=headers
    )
    
    assert response.status_code == 404
