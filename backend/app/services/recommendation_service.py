"""
Recommendation service with hybrid algorithm for personalized activity recommendations.

Implements requirements RF-014 to RF-015 from SRS.
"""
from decimal import Decimal
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select, and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis
import json

from app.models.activity import Actividad
from app.models.user import PerfilUsuario
from app.models.favorite import Favorito
from app.schemas.recommendation import (
    RecommendationResponse,
    RecommendationExplanation,
    RecommendationList,
    RecommendationQuery
)
from app.core.config import settings


class RecommendationService:
    """Service class for recommendation operations."""
    
    def __init__(self):
        """Initialize recommendation service with Redis connection."""
        self.redis_client: Optional[aioredis.Redis] = None
    
    async def _get_redis(self) -> aioredis.Redis:
        """Get or create Redis connection."""
        if self.redis_client is None:
            self.redis_client = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client
    
    async def get_recommendations(
        self,
        db: AsyncSession,
        usuario_id: Optional[int],
        query_params: RecommendationQuery,
    ) -> RecommendationList:
        """
        Get recommendations for user (RF-014, RF-015).
        
        If usuario_id is None, returns popularity-based recommendations.
        If usuario_id is provided, returns personalized recommendations.
        
        Algorithm:
        1. Base score: popularidad_normalizada (0-1)
        2. Bonus for matching tags: +10 points per matching tag
        3. Bonus for preferred locality: +5 points
        4. Bonus for preferred availability: +3 points
        5. Normalize final score to 0-100 range
        
        Uses Redis cache with 1 hour TTL.
        
        Args:
            db: Database session
            usuario_id: User ID (None for anonymous/public recommendations)
            query_params: Query parameters (limit, filters)
            
        Returns:
            List of recommendations with scores and explanations
        """
        # Build cache key (use 'anonymous' for unauthenticated users)
        user_key = f"user:{usuario_id}" if usuario_id else "anonymous"
        cache_key = f"recommendations:{user_key}:{query_params.limit}:{query_params.tipo}:{query_params.localidad}:{query_params.exclude_favorited}"
        redis = await self._get_redis()
        
        cached = await redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            return RecommendationList(**data)
        
        # Get user profile and favorites only if authenticated
        profile = None
        profile_complete = False
        favorited_ids = set()
        
        if usuario_id:
            # Get user profile
            profile_query = select(PerfilUsuario).where(PerfilUsuario.usuario_id == usuario_id)
            profile_result = await db.execute(profile_query)
            profile = profile_result.scalar_one_or_none()
            
            # Check if profile has at least one preference for personalization
            profile_complete = bool(
                profile
                and (
                    (profile.etiquetas_interes and len(profile.etiquetas_interes) > 0)
                    or profile.localidad_preferida
                    or profile.nivel_actividad
                )
            )
            
            # Get user's favorited activities (for is_favorite flag and optional exclusion)
            fav_query = select(Favorito.actividad_id).where(Favorito.usuario_id == usuario_id)
            fav_result = await db.execute(fav_query)
            favorited_ids = {fav_id for (fav_id,) in fav_result.fetchall()}
        
        # Build query for activities
        query = select(Actividad).where(Actividad.estado == "activa")
        
        # Apply filters
        if query_params.tipo:
            query = query.where(Actividad.tipo == query_params.tipo)
        if query_params.localidad:
            query = query.where(Actividad.localidad == query_params.localidad)
        if query_params.exclude_favorited and favorited_ids:
            query = query.where(~Actividad.id.in_(favorited_ids))
        
        # Get activities
        result = await db.execute(query)
        activities = result.scalars().all()
        
        # Score each activity
        scored_activities = []
        for activity in activities:
            score, explanation = await self._calculate_activity_score(
                activity=activity,
                profile=profile
            )
            
            # Check if it's favorited
            is_favorite = activity.id in favorited_ids if favorited_ids else False
            
            scored_activities.append({
                "activity": activity,
                "score": score,
                "explanation": explanation,
                "is_favorite": is_favorite
            })
        
        # Sort by score descending
        scored_activities.sort(key=lambda x: x["score"], reverse=True)
        
        # Take top N
        top_recommendations = scored_activities[:query_params.limit]
        
        # Build response
        items = []
        for rec in top_recommendations:
            activity = rec["activity"]
            items.append(
                RecommendationResponse(
                    actividad={
                        "id": str(activity.id),
                        "titulo": activity.titulo,
                        "descripcion": activity.descripcion,
                        "tipo": activity.tipo,
                        "fecha_inicio": activity.fecha_inicio.isoformat(),
                        "fecha_fin": activity.fecha_fin.isoformat() if activity.fecha_fin else None,
                        "ubicacion_direccion": activity.ubicacion_direccion,
                        "ubicacion_lat": float(activity.ubicacion_lat),
                        "ubicacion_lng": float(activity.ubicacion_lng),
                        "localidad": activity.localidad,
                        "precio": float(activity.precio),
                        "es_gratis": activity.es_gratis,
                        "nivel_actividad": activity.nivel_actividad,
                        "etiquetas": activity.etiquetas,
                        "contacto": activity.contacto,
                        "enlace_externo": activity.enlace_externo,
                        "imagen_url": activity.imagen_url,
                        "fuente": activity.fuente,
                        "estado": activity.estado,
                        "popularidad_favoritos": activity.popularidad_favoritos,
                        "popularidad_vistas": float(activity.popularidad_vistas),
                        "popularidad_normalizada": float(activity.popularidad_normalizada),
                        "created_at": activity.created_at.isoformat(),
                        "updated_at": activity.updated_at.isoformat(),
                    },
                    score=rec["score"],
                    explanation=rec["explanation"],
                    is_favorite=rec["is_favorite"]
                )
            )
        
        response = RecommendationList(
            items=items,
            total=len(items),
            user_profile_complete=profile_complete
        )
        
        # Cache for 1 hour
        await redis.setex(
            cache_key,
            3600,  # 1 hour TTL
            json.dumps(response.model_dump(), default=str)
        )
        
        return response
    
    async def _calculate_activity_score(
        self,
        activity: Actividad,
        profile: Optional[PerfilUsuario],
    ) -> tuple[float, RecommendationExplanation]:
        """
        Calculate recommendation score for an activity.
        
        Scoring algorithm:
        - Base: popularidad_normalizada * 10 (0-10 points)
        - Tag match: +10 points per matching tag
        - Locality match: +5 points
        - Activity level match: +3 points
        
        Args:
            activity: Activity to score
            profile: User profile (optional)
            
        Returns:
            Tuple of (score, explanation)
        """
        score = 0.0
        reasons = []
        
        # Base popularity score (0-10 points)
        popularity_score = float(activity.popularidad_normalizada) * 10
        score += popularity_score
        
        if popularity_score > 5:
            reasons.append(f"Popular ({activity.popularidad_favoritos} favoritos)")
        
        # If no profile, return popularity-based recommendation
        if not profile:
            explanation = RecommendationExplanation(
                reason="popular",
                details="Actividad popular en la comunidad"
            )
            return min(score, 100.0), explanation
        
        # Tag matching (+10 per matching tag, max 30)
        if profile.etiquetas_interes and activity.etiquetas:
            matching_tags = set(profile.etiquetas_interes) & set(activity.etiquetas)
            if matching_tags:
                tag_score = len(matching_tags) * 10
                score += min(tag_score, 30)  # Cap at 30 points
                reasons.append(f"{len(matching_tags)} etiquetas coinciden")
        
        # Locality match (+5 points)
        if profile.localidad_preferida and profile.localidad_preferida == activity.localidad:
            score += 5
            reasons.append(f"En {activity.localidad}")
        
        # Activity level match (+3 points)
        if profile.nivel_actividad and profile.nivel_actividad == activity.nivel_actividad:
            score += 3
            reasons.append(f"Nivel {activity.nivel_actividad}")
        
        # Generate explanation
        if not reasons:
            explanation = RecommendationExplanation(
                reason="popular",
                details="Basado en popularidad general"
            )
        else:
            # Use most significant reason
            if any("etiquetas" in r for r in reasons):
                reason = "tags"
                details = ", ".join(reasons)
            elif any("localidad" in r.lower() for r in reasons):
                reason = "location"
                details = ", ".join(reasons)
            else:
                reason = "popular"
                details = ", ".join(reasons)
            
            explanation = RecommendationExplanation(
                reason=reason,
                details=details
            )
        
        # Normalize score to 0-100
        final_score = min(score, 100.0)
        
        return final_score, explanation
    
    async def invalidate_cache(self, usuario_id: int) -> None:
        """
        Invalidate recommendation cache for user.
        
        Called when user adds/removes favorites or updates profile.
        
        Args:
            usuario_id: User ID
        """
        redis = await self._get_redis()
        
        # Delete all cache keys for this user
        pattern = f"recommendations:user:{usuario_id}:*"
        
        # Scan and delete matching keys
        cursor = 0
        while True:
            cursor, keys = await redis.scan(cursor, match=pattern, count=100)
            if keys:
                await redis.delete(*keys)
            if cursor == 0:
                break
    
    async def close(self) -> None:
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.close()


# Singleton instance
recommendation_service = RecommendationService()
