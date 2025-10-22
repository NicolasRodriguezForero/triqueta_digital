"""
Activity endpoints for CRUD, search, and filters.

Implements requirements RF-006 to RF-010 from SRS.
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_current_admin_user, get_db
from app.models.user import Usuario
from app.services.activity_service import ActivityService
from app.schemas.activity import (
    ActividadCreate,
    ActividadUpdate,
    ActividadResponse,
    ActividadListResponse,
    ActividadListItem,
    ActividadSearchQuery,
    ActividadEstadoUpdate,
    ImportResult,
)


router = APIRouter(prefix="/actividades", tags=["actividades"])


@router.get("", response_model=ActividadListResponse, summary="Listar actividades (RF-006)")
async def list_activities(
    # Search
    q: Optional[str] = Query(None, description="Búsqueda de texto libre"),
    
    # Filters
    tipo: Optional[str] = Query(None, description="Tipo: cultura, deporte, recreacion"),
    localidad: Optional[str] = Query(None, description="Localidad: Chapinero, Santa Fe, La Candelaria"),
    fecha_desde: Optional[str] = Query(None, description="Fecha desde (ISO 8601)"),
    fecha_hasta: Optional[str] = Query(None, description="Fecha hasta (ISO 8601)"),
    precio_min: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    precio_max: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    es_gratis: Optional[bool] = Query(None, description="Solo actividades gratuitas"),
    nivel_actividad: Optional[str] = Query(None, description="Nivel: bajo, medio, alto"),
    etiquetas: Optional[List[str]] = Query(None, description="Etiquetas (puede repetirse)"),
    
    # Pagination
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(20, ge=1, le=100, description="Tamaño de página"),
    
    # Sorting
    sort_by: str = Query("fecha_inicio", description="Campo para ordenar"),
    sort_order: str = Query("asc", description="Orden: asc o desc"),
    
    db: AsyncSession = Depends(get_db),
):
    """
    Lista actividades con filtros y paginación.
    
    **Acceso:** Público (no requiere autenticación)
    """
    # Build query params
    query_params = ActividadSearchQuery(
        q=q,
        tipo=tipo,
        localidad=localidad,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        precio_min=precio_min,
        precio_max=precio_max,
        es_gratis=es_gratis,
        nivel_actividad=nivel_actividad,
        etiquetas=etiquetas,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    
    activities, pagination = await ActivityService.list_activities(
        db=db,
        query_params=query_params,
    )
    
    # Convert to list items with descripcion_corta
    list_items = []
    for activity in activities:
        desc_corta = activity.descripcion[:200] + "..." if len(activity.descripcion) > 200 else activity.descripcion
        item = ActividadListItem(
            id=activity.id,
            titulo=activity.titulo,
            descripcion_corta=desc_corta,
            imagen_url=activity.imagen_url,
            fecha_inicio=activity.fecha_inicio,
            localidad=activity.localidad,
            tipo=activity.tipo,
            precio=activity.precio,
            es_gratis=activity.es_gratis,
            etiquetas=activity.etiquetas,
            popularidad_normalizada=activity.popularidad_normalizada,
        )
        list_items.append(item)
    
    return ActividadListResponse(data=list_items, pagination=pagination)


@router.get("/{activity_id}", response_model=ActividadResponse, summary="Detalle de actividad (RF-007)")
async def get_activity(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtiene el detalle completo de una actividad.
    
    **Acceso:** Público (no requiere autenticación)
    
    Registra una vista para el cálculo de popularidad.
    """
    activity = await ActivityService.get_activity_by_id(db, activity_id)
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada",
        )
    
    # Register view for popularity
    await ActivityService.register_view(db, activity_id)
    
    return activity


@router.post("", response_model=ActividadResponse, status_code=status.HTTP_201_CREATED, summary="Crear actividad (RF-009)")
async def create_activity(
    activity_data: ActividadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin_user),
):
    """
    Crea una nueva actividad.
    
    **Acceso:** Solo administradores
    """
    activity = await ActivityService.create_activity(db, activity_data)
    return activity


@router.put("/{activity_id}", response_model=ActividadResponse, summary="Actualizar actividad (RF-009)")
async def update_activity(
    activity_id: UUID,
    activity_data: ActividadUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin_user),
):
    """
    Actualiza una actividad existente.
    
    **Acceso:** Solo administradores
    """
    activity = await ActivityService.update_activity(db, activity_id, activity_data)
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada",
        )
    
    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar actividad (RF-009)")
async def delete_activity(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin_user),
):
    """
    Elimina una actividad (soft delete).
    
    **Acceso:** Solo administradores
    
    La actividad se marca como inactiva pero no se elimina de la base de datos.
    """
    deleted = await ActivityService.delete_activity(db, activity_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada",
        )
    
    return None


@router.post("/{activity_id}/aprobar", response_model=ActividadResponse, summary="Aprobar actividad (RF-018)")
async def approve_activity(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin_user),
):
    """
    Aprueba una actividad importada (cambia estado a 'activa').
    
    **Acceso:** Solo administradores
    """
    activity = await ActivityService.update_estado(db, activity_id, "activa")
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada",
        )
    
    return activity


@router.post("/{activity_id}/rechazar", response_model=ActividadResponse, summary="Rechazar actividad (RF-018)")
async def reject_activity(
    activity_id: UUID,
    estado_data: ActividadEstadoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin_user),
):
    """
    Rechaza una actividad importada (cambia estado a 'rechazada').
    
    **Acceso:** Solo administradores
    """
    activity = await ActivityService.update_estado(
        db, activity_id, "rechazada", estado_data.nota
    )
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada",
        )
    
    return activity


@router.post("/import", response_model=ImportResult, summary="Importar actividades (RF-010)")
async def import_activities(
    file: UploadFile = File(..., description="Archivo CSV o JSON"),
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin_user),
):
    """
    Importa actividades desde un archivo CSV o JSON.
    
    **Acceso:** Solo administradores
    
    Las actividades importadas se crean con estado 'pendiente_validacion'.
    """
    # TODO: Implement CSV/JSON parsing
    # For now, return placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Importación de archivos en desarrollo",
    )


@router.get("/admin/pendientes", response_model=ActividadListResponse, summary="Listar actividades pendientes (RF-018)")
async def list_pending_activities(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin_user),
):
    """
    Lista actividades pendientes de validación.
    
    **Acceso:** Solo administradores
    """
    query_params = ActividadSearchQuery(
        page=page,
        page_size=page_size,
        sort_by="created_at",
        sort_order="desc",
    )
    
    # Override estado filter to show only pending
    activities, pagination = await ActivityService.list_activities(
        db=db,
        query_params=query_params,
        include_inactive=True,
    )
    
    # Filter by estado = pendiente_validacion
    pending_activities = [a for a in activities if a.estado == "pendiente_validacion"]
    
    # Convert to list items
    list_items = []
    for activity in pending_activities:
        desc_corta = activity.descripcion[:200] + "..." if len(activity.descripcion) > 200 else activity.descripcion
        item = ActividadListItem(
            id=activity.id,
            titulo=activity.titulo,
            descripcion_corta=desc_corta,
            imagen_url=activity.imagen_url,
            fecha_inicio=activity.fecha_inicio,
            localidad=activity.localidad,
            tipo=activity.tipo,
            precio=activity.precio,
            es_gratis=activity.es_gratis,
            etiquetas=activity.etiquetas,
            popularidad_normalizada=activity.popularidad_normalizada,
        )
        list_items.append(item)
    
    # Update pagination total
    pagination.total = len(pending_activities)
    pagination.total_pages = (len(pending_activities) + page_size - 1) // page_size
    
    return ActividadListResponse(data=list_items, pagination=pagination)
