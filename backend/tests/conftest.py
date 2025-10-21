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

# Load test environment variables
load_dotenv(".env.test")

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
