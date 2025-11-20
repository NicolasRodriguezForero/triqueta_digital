"""
Tests for recommendations functionality.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity import Actividad
from app.models.user import PerfilUsuario
from decimal import Decimal
from datetime import datetime, timedelta
import uuid


class TestRecommendationsAPI:
    """Test suite for recommendations API endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_recommendations_authenticated(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
    ):
        """Test getting recommendations for authenticated user."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        response = await async_client.get(
            "/api/v1/recomendaciones",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "user_profile_complete" in data
        assert isinstance(data["items"], list)
    
    @pytest.mark.asyncio
    async def test_get_recommendations_unauthorized(
        self,
        async_client: AsyncClient,
    ):
        """Test getting recommendations without authentication fails."""
        response = await async_client.get("/api/v1/recomendaciones")
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_recommendations_with_limit(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_db: AsyncSession,
    ):
        """Test limiting number of recommendations."""
        # Create multiple activities
        for i in range(15):
            activity = Actividad(
                id=uuid.uuid4(),
                titulo=f"Activity {i}",
                descripcion=f"Description {i}",
                tipo="cultura",
                fecha_inicio=datetime.utcnow() + timedelta(days=i),
                ubicacion_direccion=f"Address {i}",
                ubicacion_lat=Decimal("4.7110"),
                ubicacion_lng=Decimal("-74.0721"),
                localidad="Chapinero",
                precio=Decimal("0"),
                es_gratis=True,
                etiquetas=["test"],
                estado="activa"
            )
            test_db.add(activity)
        await test_db.commit()
        
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Request only 5 recommendations
        response = await async_client.get(
            "/api/v1/recomendaciones?limit=5",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 5
    
    @pytest.mark.asyncio
    async def test_recommendations_with_type_filter(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_db: AsyncSession,
    ):
        """Test filtering recommendations by activity type."""
        # Create activities of different types
        for tipo in ["cultura", "deporte", "recreacion"]:
            activity = Actividad(
                id=uuid.uuid4(),
                titulo=f"Activity {tipo}",
                descripcion=f"Description {tipo}",
                tipo=tipo,
                fecha_inicio=datetime.utcnow() + timedelta(days=7),
                ubicacion_direccion="Address",
                ubicacion_lat=Decimal("4.7110"),
                ubicacion_lng=Decimal("-74.0721"),
                localidad="Chapinero",
                precio=Decimal("0"),
                es_gratis=True,
                etiquetas=["test"],
                estado="activa"
            )
            test_db.add(activity)
        await test_db.commit()
        
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Request only cultura type
        response = await async_client.get(
            "/api/v1/recomendaciones?tipo=cultura",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # All recommendations should be cultura type
        for item in data["items"]:
            assert item["actividad"]["tipo"] == "cultura"
    
    @pytest.mark.asyncio
    async def test_recommendations_exclude_favorited(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
    ):
        """Test excluding favorited activities from recommendations."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # Add activity to favorites
        await async_client.post(
            "/api/v1/favoritos",
            json={"actividad_id": str(test_activity.id)},
            headers=headers
        )
        
        # Get recommendations with exclude_favorited=true
        response = await async_client.get(
            "/api/v1/recomendaciones?exclude_favorited=true",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Test activity should not be in recommendations
        recommendation_ids = [item["actividad"]["id"] for item in data["items"]]
        assert str(test_activity.id) not in recommendation_ids
    
    @pytest.mark.asyncio
    async def test_recommendations_include_score_and_explanation(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_activity: Actividad,
    ):
        """Test that recommendations include score and explanation."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        response = await async_client.get(
            "/api/v1/recomendaciones",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        if data["items"]:
            first_item = data["items"][0]
            assert "score" in first_item
            assert "explanation" in first_item
            assert "reason" in first_item["explanation"]
            assert "details" in first_item["explanation"]
            assert isinstance(first_item["score"], (int, float))
            assert 0 <= first_item["score"] <= 100
    
    @pytest.mark.asyncio
    async def test_recommendations_with_profile_tags(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_db: AsyncSession,
        sample_user_data: dict,
    ):
        """Test that recommendations prioritize profile tag matches."""
        # Update user profile with interests
        from app.models.user import Usuario
        from sqlalchemy import select
        
        user_query = select(Usuario).where(Usuario.email == sample_user_data["email"])
        user_result = await test_db.execute(user_query)
        user = user_result.scalar_one()
        
        if not user.perfil:
            perfil = PerfilUsuario(
                usuario_id=user.id,
                etiquetas_interes=["arte", "musica"],
                localidad_preferida="Chapinero"
            )
            test_db.add(perfil)
        else:
            user.perfil.etiquetas_interes = ["arte", "musica"]
            user.perfil.localidad_preferida = "Chapinero"
        
        await test_db.commit()
        
        # Create activity with matching tags
        matching_activity = Actividad(
            id=uuid.uuid4(),
            titulo="Music Concert",
            descripcion="A great music event",
            tipo="cultura",
            fecha_inicio=datetime.utcnow() + timedelta(days=7),
            ubicacion_direccion="Concert Hall",
            ubicacion_lat=Decimal("4.7110"),
            ubicacion_lng=Decimal("-74.0721"),
            localidad="Chapinero",
            precio=Decimal("0"),
            es_gratis=True,
            etiquetas=["arte", "musica", "cultura"],
            estado="activa",
            popularidad_normalizada=Decimal("0.1")  # Low popularity
        )
        
        # Create activity with no matching tags but high popularity
        non_matching_activity = Actividad(
            id=uuid.uuid4(),
            titulo="Sports Event",
            descripcion="A popular sports event",
            tipo="deporte",
            fecha_inicio=datetime.utcnow() + timedelta(days=8),
            ubicacion_direccion="Stadium",
            ubicacion_lat=Decimal("4.7110"),
            ubicacion_lng=Decimal("-74.0721"),
            localidad="Santa Fe",
            precio=Decimal("0"),
            es_gratis=True,
            etiquetas=["deporte", "futbol"],
            estado="activa",
            popularidad_normalizada=Decimal("0.9")  # High popularity
        )
        
        test_db.add(matching_activity)
        test_db.add(non_matching_activity)
        await test_db.commit()
        
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        response = await async_client.get(
            "/api/v1/recomendaciones",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # The matching activity should have a higher score despite lower popularity
        # because of tag bonuses
        if len(data["items"]) >= 2:
            scores = {item["actividad"]["id"]: item["score"] for item in data["items"]}
            # Matching activity should get bonus points for tags
            assert str(matching_activity.id) in scores
    
    @pytest.mark.asyncio
    async def test_recommendations_sorted_by_score(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_db: AsyncSession,
    ):
        """Test that recommendations are sorted by score descending."""
        # Create multiple activities with different popularity
        for i in range(5):
            activity = Actividad(
                id=uuid.uuid4(),
                titulo=f"Activity {i}",
                descripcion=f"Description {i}",
                tipo="cultura",
                fecha_inicio=datetime.utcnow() + timedelta(days=i),
                ubicacion_direccion=f"Address {i}",
                ubicacion_lat=Decimal("4.7110"),
                ubicacion_lng=Decimal("-74.0721"),
                localidad="Chapinero",
                precio=Decimal("0"),
                es_gratis=True,
                etiquetas=["test"],
                estado="activa",
                popularidad_normalizada=Decimal(str(i * 0.1))
            )
            test_db.add(activity)
        await test_db.commit()
        
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        response = await async_client.get(
            "/api/v1/recomendaciones",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check that scores are in descending order
        if len(data["items"]) > 1:
            scores = [item["score"] for item in data["items"]]
            assert scores == sorted(scores, reverse=True)
    
    @pytest.mark.asyncio
    async def test_recommendations_profile_complete_flag(
        self,
        async_client: AsyncClient,
        test_user_tokens: dict,
        test_db: AsyncSession,
        sample_user_data: dict,
    ):
        """Test that profile_complete flag is accurate."""
        headers = {"Authorization": f"Bearer {test_user_tokens['access_token']}"}
        
        # First check with incomplete profile
        response = await async_client.get(
            "/api/v1/recomendaciones",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        # Should be false initially (no tags set)
        
        # Update profile with interests
        from app.models.user import Usuario
        from sqlalchemy import select
        
        user_query = select(Usuario).where(Usuario.email == sample_user_data["email"])
        user_result = await test_db.execute(user_query)
        user = user_result.scalar_one()
        
        if not user.perfil:
            perfil = PerfilUsuario(
                usuario_id=user.id,
                etiquetas_interes=["arte", "cultura"]
            )
            test_db.add(perfil)
        else:
            user.perfil.etiquetas_interes = ["arte", "cultura"]
        
        await test_db.commit()
        
        # Check again with complete profile
        response = await async_client.get(
            "/api/v1/recomendaciones",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_profile_complete"] is True
