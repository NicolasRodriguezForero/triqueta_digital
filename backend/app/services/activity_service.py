"""
Activity service with business logic for CRUD, search, and filters.

Implements requirements RF-006 to RF-010 from SRS.
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from sqlalchemy import select, func, or_, and_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.activity import Actividad
from app.schemas.activity import (
    ActividadCreate,
    ActividadUpdate,
    ActividadSearchQuery,
    PaginationMetadata,
)


class ActivityService:
    """Service class for activity operations."""
    
    @staticmethod
    async def create_activity(
        db: AsyncSession,
        activity_data: ActividadCreate,
    ) -> Actividad:
        """
        Create a new activity (RF-009).
        
        Args:
            db: Database session
            activity_data: Activity creation data
            
        Returns:
            Created activity
        """
        activity = Actividad(**activity_data.to_db_dict())
        db.add(activity)
        await db.commit()
        await db.refresh(activity)
        return activity
    
    @staticmethod
    async def get_activity_by_id(
        db: AsyncSession,
        activity_id: UUID,
        include_inactive: bool = False,
    ) -> Optional[Actividad]:
        """
        Get activity by ID (RF-007).
        
        Args:
            db: Database session
            activity_id: Activity UUID
            include_inactive: Include activities with estado != 'activa'
            
        Returns:
            Activity if found, None otherwise
        """
        query = select(Actividad).where(Actividad.id == activity_id)
        
        if not include_inactive:
            query = query.where(Actividad.estado == "activa")
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_activity(
        db: AsyncSession,
        activity_id: UUID,
        activity_data: ActividadUpdate,
    ) -> Optional[Actividad]:
        """
        Update an existing activity (RF-009).
        
        Args:
            db: Database session
            activity_id: Activity UUID
            activity_data: Activity update data
            
        Returns:
            Updated activity if found, None otherwise
        """
        activity = await ActivityService.get_activity_by_id(
            db, activity_id, include_inactive=True
        )
        
        if not activity:
            return None
        
        # Update only provided fields
        update_data = activity_data.to_db_dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(activity, field, value)
        
        activity.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(activity)
        return activity
    
    @staticmethod
    async def delete_activity(
        db: AsyncSession,
        activity_id: UUID,
    ) -> bool:
        """
        Soft delete an activity by setting estado to 'inactiva' (RF-009).
        
        Args:
            db: Database session
            activity_id: Activity UUID
            
        Returns:
            True if deleted, False if not found
        """
        activity = await ActivityService.get_activity_by_id(
            db, activity_id, include_inactive=True
        )
        
        if not activity:
            return False
        
        activity.estado = "inactiva"
        activity.updated_at = datetime.utcnow()
        await db.commit()
        return True
    
    @staticmethod
    async def list_activities(
        db: AsyncSession,
        query_params: ActividadSearchQuery,
        include_inactive: bool = False,
    ) -> Tuple[List[Actividad], PaginationMetadata]:
        """
        List activities with filters and pagination (RF-006, RF-008).
        
        Args:
            db: Database session
            query_params: Search and filter parameters
            include_inactive: Include activities with estado != 'activa'
            
        Returns:
            Tuple of (activities list, pagination metadata)
        """
        # Base query
        query = select(Actividad)
        
        # Filter by estado
        if not include_inactive:
            query = query.where(Actividad.estado == "activa")
        
        # Apply filters
        query = ActivityService._apply_filters(query, query_params)
        
        # Apply search
        if query_params.q:
            query = ActivityService._apply_search(query, query_params.q)
        
        # Count total for pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply sorting
        query = ActivityService._apply_sorting(query, query_params.sort_by, query_params.sort_order)
        
        # Apply pagination
        offset = (query_params.page - 1) * query_params.page_size
        query = query.offset(offset).limit(query_params.page_size)
        
        # Execute query
        result = await db.execute(query)
        activities = result.scalars().all()
        
        # Build pagination metadata
        total_pages = (total + query_params.page_size - 1) // query_params.page_size
        pagination = PaginationMetadata(
            total=total,
            page=query_params.page,
            page_size=query_params.page_size,
            total_pages=total_pages,
        )
        
        return list(activities), pagination
    
    @staticmethod
    def _apply_filters(query, params: ActividadSearchQuery):
        """Apply filters to query based on search parameters."""
        
        if params.tipo:
            query = query.where(Actividad.tipo == params.tipo)
        
        if params.localidad:
            query = query.where(Actividad.localidad == params.localidad)
        
        if params.fecha_desde:
            query = query.where(Actividad.fecha_inicio >= params.fecha_desde)
        
        if params.fecha_hasta:
            query = query.where(Actividad.fecha_inicio <= params.fecha_hasta)
        
        if params.precio_min is not None:
            query = query.where(Actividad.precio >= params.precio_min)
        
        if params.precio_max is not None:
            query = query.where(Actividad.precio <= params.precio_max)
        
        if params.es_gratis is not None:
            query = query.where(Actividad.es_gratis == params.es_gratis)
        
        if params.nivel_actividad:
            query = query.where(Actividad.nivel_actividad == params.nivel_actividad)
        
        if params.etiquetas:
            # Activity must have at least one of the specified tags
            query = query.where(
                or_(*[Actividad.etiquetas.contains([tag]) for tag in params.etiquetas])
            )
        
        return query
    
    @staticmethod
    def _apply_search(query, search_query: str):
        """
        Apply full-text search to query (RF-008).
        
        Searches in: titulo, descripcion, etiquetas.
        """
        search_term = f"%{search_query.lower()}%"
        
        query = query.where(
            or_(
                func.lower(Actividad.titulo).like(search_term),
                func.lower(Actividad.descripcion).like(search_term),
                func.array_to_string(Actividad.etiquetas, ' ').ilike(search_term),
            )
        )
        
        return query
    
    @staticmethod
    def _apply_sorting(query, sort_by: str, sort_order: str):
        """Apply sorting to query."""
        
        # Map sort fields to model attributes
        sort_fields = {
            "fecha_inicio": Actividad.fecha_inicio,
            "popularidad": Actividad.popularidad_normalizada,
            "precio": Actividad.precio,
            "titulo": Actividad.titulo,
            "tipo": Actividad.tipo,
            "localidad": Actividad.localidad,
            "estado": Actividad.estado,
        }
        
        sort_field = sort_fields.get(sort_by, Actividad.fecha_inicio)
        
        if sort_order == "desc":
            query = query.order_by(desc(sort_field))
        else:
            query = query.order_by(asc(sort_field))
        
        return query
    
    @staticmethod
    async def register_view(
        db: AsyncSession,
        activity_id: UUID,
        user_id: Optional[int] = None,
    ) -> bool:
        """
        Register a view for popularity calculation (RF-015).
        
        Increments popularidad_vistas by 0.1, max 1 per user per day.
        
        Args:
            db: Database session
            activity_id: Activity UUID
            user_id: User ID (optional, for anonymous views)
            
        Returns:
            True if view was registered
        """
        activity = await ActivityService.get_activity_by_id(db, activity_id)
        
        if not activity:
            return False
        
        # TODO: Implement check for 1 view per user per day using Redis or separate table
        # For MVP, we increment directly
        activity.popularidad_vistas += Decimal("0.1")
        activity.updated_at = datetime.utcnow()
        
        await db.commit()
        return True
    
    @staticmethod
    async def update_estado(
        db: AsyncSession,
        activity_id: UUID,
        estado: str,
        nota: Optional[str] = None,
    ) -> Optional[Actividad]:
        """
        Update activity estado (RF-018).
        
        Used by admin to approve/reject imported activities.
        
        Args:
            db: Database session
            activity_id: Activity UUID
            estado: New estado (activa, rechazada)
            nota: Optional note
            
        Returns:
            Updated activity if found
        """
        activity = await ActivityService.get_activity_by_id(
            db, activity_id, include_inactive=True
        )
        
        if not activity:
            return None
        
        activity.estado = estado
        activity.updated_at = datetime.utcnow()
        
        # TODO: Store nota in a separate audit table if needed
        
        await db.commit()
        await db.refresh(activity)
        return activity
    
    @staticmethod
    async def calculate_normalized_popularity(db: AsyncSession) -> None:
        """
        Calculate normalized popularity for all activities (RF-015).
        
        Score = (favoritos * 1.0 + vistas * 0.1) / max_score_in_system
        
        This should be run as a background job daily.
        """
        # Get max popularity score
        max_query = select(
            func.max(Actividad.popularidad_favoritos + (Actividad.popularidad_vistas * Decimal("0.1")))
        )
        result = await db.execute(max_query)
        max_score = result.scalar() or Decimal("1.0")
        
        # Update all activities
        activities_query = select(Actividad)
        result = await db.execute(activities_query)
        activities = result.scalars().all()
        
        for activity in activities:
            raw_score = (
                Decimal(activity.popularidad_favoritos) + 
                (activity.popularidad_vistas * Decimal("0.1"))
            )
            activity.popularidad_normalizada = raw_score / max_score if max_score > 0 else Decimal("0")
        
        await db.commit()
    
    @staticmethod
    async def import_from_csv(
        db: AsyncSession,
        activities_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Import activities from CSV/JSON data (RF-010).
        
        Args:
            db: Database session
            activities_data: List of activity dictionaries
            
        Returns:
            Import result summary
        """
        total_procesados = len(activities_data)
        exitosos = 0
        duplicados = 0
        errores = 0
        errores_detalle = []
        
        for idx, data in enumerate(activities_data, start=1):
            try:
                # Check for duplicates (titulo + fecha_inicio + ubicacion)
                duplicate_query = select(Actividad).where(
                    and_(
                        Actividad.titulo == data.get("titulo"),
                        Actividad.fecha_inicio == data.get("fecha_inicio"),
                        Actividad.ubicacion_direccion == data.get("ubicacion_direccion"),
                    )
                )
                result = await db.execute(duplicate_query)
                existing = result.scalar_one_or_none()
                
                if existing:
                    duplicados += 1
                    continue
                
                # Create activity with estado = 'pendiente_validacion'
                activity_data = ActividadCreate(**data, estado="pendiente_validacion")
                activity = Actividad(**activity_data.to_db_dict())
                db.add(activity)
                exitosos += 1
                
            except Exception as e:
                errores += 1
                errores_detalle.append({
                    "fila": idx,
                    "error": str(e),
                })
        
        await db.commit()
        
        return {
            "total_procesados": total_procesados,
            "exitosos": exitosos,
            "duplicados": duplicados,
            "errores": errores,
            "errores_detalle": errores_detalle,
        }
