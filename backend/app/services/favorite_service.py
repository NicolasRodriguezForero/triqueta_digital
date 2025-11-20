"""
Favorite service with business logic for managing user favorites.

Implements requirements RF-011 to RF-013 from SRS.
"""
from datetime import datetime
from uuid import UUID
from typing import Optional, Tuple
from sqlalchemy import select, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.models.favorite import Favorito
from app.models.activity import Actividad
from app.schemas.favorite import FavoritoCreate, FavoritoResponse, FavoritoWithActivity, FavoritoList


class FavoriteService:
    """Service class for favorite operations."""
    
    @staticmethod
    async def add_favorite(
        db: AsyncSession,
        usuario_id: int,
        favorito_data: FavoritoCreate,
    ) -> FavoritoResponse:
        """
        Add activity to user's favorites (RF-011).
        
        Args:
            db: Database session
            usuario_id: User ID
            favorito_data: Favorite creation data
            
        Returns:
            Created favorite
            
        Raises:
            IntegrityError: If favorite already exists
            ValueError: If activity not found
        """
        # Check if activity exists
        activity_query = select(Actividad).where(
            and_(
                Actividad.id == favorito_data.actividad_id,
                Actividad.estado == "activa"
            )
        )
        result = await db.execute(activity_query)
        activity = result.scalar_one_or_none()
        
        if not activity:
            raise ValueError("Activity not found or not active")
        
        # Create favorite
        favorito = Favorito(
            usuario_id=usuario_id,
            actividad_id=favorito_data.actividad_id,
        )
        
        try:
            db.add(favorito)
            await db.flush()
            
            # Update activity favorite count
            activity.popularidad_favoritos += 1
            await db.commit()
            await db.refresh(favorito)
            
            return FavoritoResponse.model_validate(favorito)
        except IntegrityError:
            await db.rollback()
            raise ValueError("Activity already in favorites")
    
    @staticmethod
    async def remove_favorite(
        db: AsyncSession,
        usuario_id: int,
        actividad_id: UUID,
    ) -> bool:
        """
        Remove activity from user's favorites (RF-012).
        
        Args:
            db: Database session
            usuario_id: User ID
            actividad_id: Activity UUID
            
        Returns:
            True if removed, False if not found
        """
        # Find favorite
        query = select(Favorito).where(
            and_(
                Favorito.usuario_id == usuario_id,
                Favorito.actividad_id == actividad_id
            )
        )
        result = await db.execute(query)
        favorito = result.scalar_one_or_none()
        
        if not favorito:
            return False
        
        # Get activity to update count
        activity_query = select(Actividad).where(Actividad.id == actividad_id)
        activity_result = await db.execute(activity_query)
        activity = activity_result.scalar_one_or_none()
        
        # Delete favorite
        await db.delete(favorito)
        
        # Update activity favorite count
        if activity and activity.popularidad_favoritos > 0:
            activity.popularidad_favoritos -= 1
        
        await db.commit()
        return True
    
    @staticmethod
    async def get_user_favorites(
        db: AsyncSession,
        usuario_id: int,
        page: int = 1,
        page_size: int = 20,
        tipo: Optional[str] = None,
        localidad: Optional[str] = None,
    ) -> FavoritoList:
        """
        Get user's favorite activities with pagination and filters (RF-013).
        
        Args:
            db: Database session
            usuario_id: User ID
            page: Page number (1-indexed)
            page_size: Items per page
            tipo: Filter by activity type
            localidad: Filter by locality
            
        Returns:
            Paginated list of favorites with activity details
        """
        # Build base query
        query = (
            select(Favorito)
            .where(Favorito.usuario_id == usuario_id)
            .options(selectinload(Favorito.actividad))
            .order_by(Favorito.fecha_guardado.desc())
        )
        
        # Apply filters via join if needed
        if tipo or localidad:
            query = query.join(Actividad)
            
            if tipo:
                query = query.where(Actividad.tipo == tipo)
            if localidad:
                query = query.where(Actividad.localidad == localidad)
        
        # Get total count
        count_query = select(func.count()).select_from(Favorito).where(
            Favorito.usuario_id == usuario_id
        )
        if tipo or localidad:
            count_query = count_query.join(Actividad)
            if tipo:
                count_query = count_query.where(Actividad.tipo == tipo)
            if localidad:
                count_query = count_query.where(Actividad.localidad == localidad)
        
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # Execute query
        result = await db.execute(query)
        favoritos = result.scalars().all()
        
        # Convert to response schema
        items = []
        for fav in favoritos:
            fav_dict = {
                "id": fav.id,
                "usuario_id": fav.usuario_id,
                "actividad_id": fav.actividad_id,
                "fecha_guardado": fav.fecha_guardado,
                "actividad": {
                    "id": str(fav.actividad.id),
                    "titulo": fav.actividad.titulo,
                    "descripcion": fav.actividad.descripcion,
                    "tipo": fav.actividad.tipo,
                    "fecha_inicio": fav.actividad.fecha_inicio.isoformat(),
                    "fecha_fin": fav.actividad.fecha_fin.isoformat() if fav.actividad.fecha_fin else None,
                    "ubicacion_direccion": fav.actividad.ubicacion_direccion,
                    "ubicacion_lat": float(fav.actividad.ubicacion_lat),
                    "ubicacion_lng": float(fav.actividad.ubicacion_lng),
                    "localidad": fav.actividad.localidad,
                    "precio": float(fav.actividad.precio),
                    "es_gratis": fav.actividad.es_gratis,
                    "nivel_actividad": fav.actividad.nivel_actividad,
                    "etiquetas": fav.actividad.etiquetas,
                    "contacto": fav.actividad.contacto,
                    "enlace_externo": fav.actividad.enlace_externo,
                    "imagen_url": fav.actividad.imagen_url,
                    "fuente": fav.actividad.fuente,
                    "estado": fav.actividad.estado,
                    "popularidad_favoritos": fav.actividad.popularidad_favoritos,
                    "popularidad_vistas": float(fav.actividad.popularidad_vistas),
                    "popularidad_normalizada": float(fav.actividad.popularidad_normalizada),
                    "created_at": fav.actividad.created_at.isoformat(),
                    "updated_at": fav.actividad.updated_at.isoformat(),
                } if fav.actividad else None
            }
            items.append(FavoritoWithActivity.model_validate(fav_dict))
        
        total_pages = (total + page_size - 1) // page_size
        
        return FavoritoList(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    @staticmethod
    async def is_favorite(
        db: AsyncSession,
        usuario_id: int,
        actividad_id: UUID,
    ) -> Tuple[bool, Optional[UUID]]:
        """
        Check if activity is in user's favorites.
        
        Args:
            db: Database session
            usuario_id: User ID
            actividad_id: Activity UUID
            
        Returns:
            Tuple of (is_favorite: bool, favorito_id: Optional[UUID])
        """
        query = select(Favorito).where(
            and_(
                Favorito.usuario_id == usuario_id,
                Favorito.actividad_id == actividad_id
            )
        )
        result = await db.execute(query)
        favorito = result.scalar_one_or_none()
        
        if favorito:
            return True, favorito.id
        return False, None
    
    @staticmethod
    async def get_favorite_count(
        db: AsyncSession,
        usuario_id: int,
    ) -> int:
        """
        Get total count of user's favorites.
        
        Args:
            db: Database session
            usuario_id: User ID
            
        Returns:
            Total favorite count
        """
        query = select(func.count()).select_from(Favorito).where(
            Favorito.usuario_id == usuario_id
        )
        result = await db.execute(query)
        return result.scalar()
