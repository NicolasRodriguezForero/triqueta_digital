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
from app.services import activity_import_service
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
    Solo muestra actividades con estado 'activa'.
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
            popularidad_favoritos=activity.popularidad_favoritos,
            popularidad_vistas=activity.popularidad_vistas,
            popularidad_normalizada=activity.popularidad_normalizada,
            estado=activity.estado,
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


@router.get("/admin/all", response_model=ActividadListResponse, summary="Listar todas las actividades (Admin)")
async def list_all_activities_admin(
    # Search
    q: Optional[str] = Query(None, description="Búsqueda de texto libre"),
    
    # Filters
    tipo: Optional[str] = Query(None, description="Tipo: cultura, deporte, recreacion"),
    localidad: Optional[str] = Query(None, description="Localidad: Chapinero, Santa Fe, La Candelaria"),
    estado: Optional[str] = Query(None, description="Filtrar por estado: activa, pendiente_validacion, rechazada, inactiva"),
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
    current_user: Usuario = Depends(get_current_admin_user),
):
    """
    Lista todas las actividades para administradores (incluye todos los estados).
    
    **Acceso:** Solo administradores
    """
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
    
    # Get all activities including inactive
    activities, pagination = await ActivityService.list_activities(
        db=db,
        query_params=query_params,
        include_inactive=True,
    )
    
    # Filter by estado if provided
    if estado:
        activities = [a for a in activities if a.estado == estado]
        pagination.total = len(activities)
        pagination.total_pages = (len(activities) + page_size - 1) // page_size
    
    # Convert to list items
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
            popularidad_favoritos=activity.popularidad_favoritos,
            popularidad_vistas=activity.popularidad_vistas,
            popularidad_normalizada=activity.popularidad_normalizada,
            estado=activity.estado,
        )
        list_items.append(item)
    
    return ActividadListResponse(data=list_items, pagination=pagination)


@router.post("/import", response_model=ImportResult, summary="Importar actividades desde CSV/JSON (RF-010)")
async def import_activities(
    file: UploadFile = File(...),
    skip_duplicates: bool = Query(True, description="Skip duplicate activities"),
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin_user)
):
    """
    Import activities from CSV or JSON file.
    
    **Admin only**
    
    CSV format:
    - titulo,descripcion,tipo,fecha_inicio,ubicacion_direccion,ubicacion_lat,ubicacion_lng,localidad,precio,es_gratis,etiquetas
    - etiquetas separated by semicolons (;)
    
    JSON format:
    - Array of activity objects with same fields as ActividadCreate
    
    Returns import statistics.
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    file_ext = file.filename.lower().split('.')[-1]
    if file_ext not in ['csv', 'json']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be CSV or JSON"
        )
    
    # Read file content
    try:
        content = await file.read()
        content_str = content.decode('utf-8')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error reading file: {str(e)}"
        )
    
    # Parse file
    try:
        if file_ext == 'csv':
            activities = activity_import_service.parse_csv(content_str)
        else:
            activities = activity_import_service.parse_json(content_str)
    except activity_import_service.ImportError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    total_activities = len(activities)
    
    # Check for duplicates
    if skip_duplicates:
        unique_activities, duplicates = await activity_import_service.check_duplicates(db, activities)
    else:
        unique_activities = activities
        duplicates = []
    
    # Validate activities
    valid_activities, validation_errors = await activity_import_service.validate_activities(unique_activities)
    
    # Import valid activities
    try:
        imported_count = await activity_import_service.import_activities(db, valid_activities, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing activities: {str(e)}"
        )
    
    # Build result
    errors_detail = []
    for error in validation_errors:
        errors_detail.append({"error": error})
    for dup in duplicates:
        errors_detail.append({"error": f"Duplicate activity: {dup}"})
    
    return ImportResult(
        total=total_activities,
        exitosos=imported_count,
        duplicados=len(duplicates),
        errores=len(validation_errors),
        errores_detalle=errors_detail
    )
