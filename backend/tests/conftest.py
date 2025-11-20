"""
Pytest configuration and fixtures.
"""
import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
from app.core.config import settings

# Load test environment variables
load_dotenv(".env.test")
# Disable rate limiting during tests to avoid Redis calls and event loop issues
settings.RATE_LIMIT_ENABLED = False

from app.main import app
from app.core.dependencies import get_db
from app.db.base import Base


# Test database URL (PostgreSQL for tests - supports ARRAY columns)
# Uses same DB as dev but with a test schema prefix (or separate test DB)
TEST_DATABASE_URL = "postgresql+asyncpg://triqueta_user:triqueta_pass@db:5432/triqueta_test"


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture to create a test database session.
    Creates tables before each test and drops them after.
    Each test gets a fresh engine to avoid event loop issues.
    """
    # Create engine for this test
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool  # Use NullPool to avoid connection pooling issues between tests
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = sessionmaker(
        engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # Dispose engine
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture to create a test HTTP client.
    Rate limiting is disabled via .env.test (RATE_LIMIT_ENABLED=False).
    """
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for tests."""
    return {
        "email": "test@example.com",
        "password": "Test1234",
        "nombre_completo": "Test User"
    }


@pytest_asyncio.fixture
async def test_user_tokens(client: AsyncClient, sample_user_data: dict) -> dict:
    """
    Fixture to create a test user and return their auth tokens.
    """
    # Register user
    await client.post("/api/v1/auth/register", json=sample_user_data)
    
    # Login to get tokens
    login_response = await client.post("/api/v1/auth/login", json={
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    })
    
    return login_response.json()


@pytest_asyncio.fixture
async def test_activity(db_session: AsyncSession):
    """
    Fixture to create a test activity.
    """
    from app.models.activity import Actividad
    from datetime import datetime, timedelta
    from decimal import Decimal
    import uuid
    
    activity = Actividad(
        id=uuid.uuid4(),
        titulo="Test Activity",
        descripcion="This is a test activity for unit testing",
        tipo="cultura",
        fecha_inicio=datetime.utcnow() + timedelta(days=7),
        fecha_fin=datetime.utcnow() + timedelta(days=8),
        ubicacion_direccion="Calle 123 #45-67",
        ubicacion_lat=Decimal("4.7110"),
        ubicacion_lng=Decimal("-74.0721"),
        localidad="Chapinero",
        precio=Decimal("0"),
        es_gratis=True,
        nivel_actividad="medio",
        etiquetas=["arte", "cultura", "gratis"],
        contacto="test@example.com",
        fuente="manual",
        estado="activa"
    )
    
    db_session.add(activity)
    await db_session.commit()
    await db_session.refresh(activity)
    
    return activity


@pytest_asyncio.fixture
async def test_db(db_session: AsyncSession) -> AsyncSession:
    """Alias for db_session for clearer test code."""
    return db_session


@pytest_asyncio.fixture
async def async_client(client: AsyncClient) -> AsyncClient:
    """Alias for client fixture for clearer test code."""
    return client

