"""
Tests for favorites functionality.
"""
import pytest
from uuid import UUID
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Actividad
from app.models.favorite import Favorito


class TestFavoritesAPI:
    """Test suite for favorites API endpoints."""
    
    @pytest.mark.asyncio
    async def test_add_favorite_success(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
    ):
        """Test successfully adding an activity to favorites."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        response = await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
            headers=headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["actividad_id"] == str(test_activity.id)
        assert "fecha_guardado" in data
    
    @pytest.mark.asyncio
    async def test_add_favorite_duplicate(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
    ):
        """Test adding duplicate favorite returns error."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Add first time
        await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
            headers=headers
        )
        
        # Try to add again
        response = await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
            headers=headers
        )
        
        assert response.status_code == 400
        assert "already in favorites" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_add_favorite_invalid_activity(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
    ):
        """Test adding non-existent activity returns error."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Random UUID
        fake_id = "12345678-1234-5678-1234-567812345678"
        
        response = await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": fake_id},
            headers=headers
        )
        
        assert response.status_code == 400
        assert "not found" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_add_favorite_unauthorized(
        self,
        async_client: AsyncClient,
        test_activity: Actividad,
    ):
        """Test adding favorite without authentication fails."""
        response = await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
        )
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_list_favorites(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
        test_db: AsyncSession,
    ):
        """Test listing user's favorites."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Add favorite first
        await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
            headers=headers
        )
        
        # List favorites
        response = await async_client.get(
            "/api/v1/favoritos",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert data["total"] >= 1
        assert len(data["items"]) >= 1
        
        # Check activity details are included
        favorite = data["items"][0]
        assert "actividad" in favorite
        assert favorite["actividad"]["id"] == str(test_activity.id)
    
    @pytest.mark.asyncio
    async def test_list_favorites_with_filters(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
    ):
        """Test listing favorites with type filter."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Add favorite
        await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
            headers=headers
        )
        
        # List with matching filter
        response = await async_client.get(
            f"/api/v1/favoritos?tipo={test_activity.tipo}",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        
        # List with non-matching filter
        response = await async_client.get(
            "/api/v1/favoritos?tipo=nonexistent",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
    
    @pytest.mark.asyncio
    async def test_remove_favorite(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
    ):
        """Test removing a favorite."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Add favorite first
        await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
            headers=headers
        )
        
        # Remove favorite
        response = await async_client.delete(
            f"/api/v1/favoritos/{test_activity.id}",
            headers=headers
        )
        
        assert response.status_code == 204
        
        # Verify it's gone
        list_response = await async_client.get(
            "/api/v1/favoritos",
            headers=headers
        )
        data = list_response.json()
        favorite_ids = [item["actividad_id"] for item in data["items"]]
        assert str(test_activity.id) not in favorite_ids
    
    @pytest.mark.asyncio
    async def test_remove_favorite_not_found(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
    ):
        """Test removing non-existent favorite returns 404."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        fake_id = "12345678-1234-5678-1234-567812345678"
        
        response = await async_client.delete(
            f"/api/v1/favoritos/{fake_id}",
            headers=headers
        )
        
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_check_is_favorite(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
    ):
        """Test checking if activity is favorited."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Check before adding (should be false)
        response = await async_client.get(
            f"/api/v1/favoritos/check/{test_activity.id}",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_favorite"] is False
        assert data["favorito_id"] is None
        
        # Add favorite
        await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
            headers=headers
        )
        
        # Check after adding (should be true)
        response = await async_client.get(
            f"/api/v1/favoritos/check/{test_activity.id}",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_favorite"] is True
        assert data["favorito_id"] is not None
    
    @pytest.mark.asyncio
    async def test_get_favorite_count(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
    ):
        """Test getting total favorite count."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Count before adding
        response = await async_client.get(
            "/api/v1/favoritos/count",
            headers=headers
        )
        
        assert response.status_code == 200
        initial_count = response.json()["count"]
        
        # Add favorite
        await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
            headers=headers
        )
       
       # Count after adding
        response = await async_client.get(
            "/api/v1/favoritos/count",
            headers=headers
        )
        
        assert response.status_code == 200
        new_count = response.json()["count"]
        assert new_count == initial_count + 1
    
    @pytest.mark.asyncio
    async def test_favorite_updates_activity_count(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
        test_db: AsyncSession,
    ):
        """Test that adding/removing favorite updates activity counter."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Get initial count
        await test_db.refresh(test_activity)
        initial_count = test_activity.popularidad_favoritos
        
        # Add favorite
        await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
            headers=headers
        )
        
        # Check count increased
        await test_db.refresh(test_activity)
        assert test_activity.popularidad_favoritos == initial_count + 1
        
        # Remove favorite
        await async_client.delete(
            f"/api/v1/favoritos/{test_activity.id}",
            headers=headers
        )
        
        # Check count decreased
        await test_db.refresh(test_activity)
        assert test_activity.popularidad_favoritos == initial_count
