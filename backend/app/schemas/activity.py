"""
Pydantic schemas for Activity endpoints.

Implements data validation for RF-006 to RF-010.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, HttpUrl


# Enums for validation
TIPOS_ACTIVIDAD = ["cultura", "deporte", "recreacion"]
LOCALIDADES = ["Chapinero", "Santa Fe", "La Candelaria"]
NIVELES_ACTIVIDAD = ["bajo", "medio", "alto"]
ESTADOS = ["activa", "pendiente_validacion", "rechazada", "inactiva"]


class ActividadBase(BaseModel):
    """Base schema for Activity with common fields."""
    titulo: str = Field(..., min_length=3, max_length=255)
    descripcion: str = Field(..., min_length=10)
    tipo: str = Field(...)
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    ubicacion_direccion: str = Field(..., min_length=5, max_length=500)
    ubicacion_lat: Decimal = Field(..., ge=-90, le=90)
    ubicacion_lng: Decimal = Field(..., ge=-180, le=180)
    localidad: str = Field(...)
    precio: Decimal = Field(default=0, ge=0)
    es_gratis: bool = Field(default=True)
    nivel_actividad: Optional[str] = None
    etiquetas: List[str] = Field(..., min_length=1)
    contacto: Optional[str] = Field(None, max_length=255)
    enlace_externo: Optional[HttpUrl] = None
    imagen_url: Optional[HttpUrl] = None
    
    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        if v not in TIPOS_ACTIVIDAD:
            raise ValueError(f"Tipo debe ser uno de: {', '.join(TIPOS_ACTIVIDAD)}")
        return v
    
    @field_validator('localidad')
    @classmethod
    def validate_localidad(cls, v):
        if v not in LOCALIDADES:
            raise ValueError(f"Localidad debe ser una de: {', '.join(LOCALIDADES)}")
        return v
    
    @field_validator('nivel_actividad')
    @classmethod
    def validate_nivel_actividad(cls, v):
        if v is not None and v not in NIVELES_ACTIVIDAD:
            raise ValueError(f"Nivel de actividad debe ser uno de: {', '.join(NIVELES_ACTIVIDAD)}")
        return v
    
    @field_validator('etiquetas')
    @classmethod
    def validate_etiquetas(cls, v):
        if len(v) > 10:
            raise ValueError("Máximo 10 etiquetas permitidas")
        return [tag.lower().strip() for tag in v]
    
    @field_validator('fecha_fin')
    @classmethod
    def validate_fecha_fin(cls, v, info):
        if v and 'fecha_inicio' in info.data and v < info.data['fecha_inicio']:
            raise ValueError("fecha_fin debe ser posterior a fecha_inicio")
        return v
    
    @field_validator('precio')
    @classmethod
    def validate_precio(cls, v, info):
        if v > 0 and info.data.get('es_gratis', False):
            raise ValueError("Una actividad gratuita no puede tener precio > 0")
        return v
    
    def to_db_dict(self):
        """Convert to dict for database, converting HttpUrl to str."""
        data = self.model_dump()
        if data.get('enlace_externo'):
            data['enlace_externo'] = str(data['enlace_externo'])
        if data.get('imagen_url'):
            data['imagen_url'] = str(data['imagen_url'])
        return data


class ActividadCreate(ActividadBase):
    """Schema for creating a new Activity (RF-009)."""
    fuente: str = Field(default="manual", max_length=100)
    estado: str = Field(default="activa")
    
    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        if v not in ESTADOS:
            raise ValueError(f"Estado debe ser uno de: {', '.join(ESTADOS)}")
        return v


class ActividadUpdate(BaseModel):
    """Schema for updating an existing Activity (RF-009)."""
    titulo: Optional[str] = Field(None, min_length=3, max_length=255)
    descripcion: Optional[str] = Field(None, min_length=10)
    tipo: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    ubicacion_direccion: Optional[str] = Field(None, min_length=5, max_length=500)
    ubicacion_lat: Optional[Decimal] = Field(None, ge=-90, le=90)
    ubicacion_lng: Optional[Decimal] = Field(None, ge=-180, le=180)
    localidad: Optional[str] = None
    precio: Optional[Decimal] = Field(None, ge=0)
    es_gratis: Optional[bool] = None
    nivel_actividad: Optional[str] = None
    etiquetas: Optional[List[str]] = None
    contacto: Optional[str] = Field(None, max_length=255)
    enlace_externo: Optional[HttpUrl] = None
    imagen_url: Optional[HttpUrl] = None
    estado: Optional[str] = None
    
    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        if v is not None and v not in TIPOS_ACTIVIDAD:
            raise ValueError(f"Tipo debe ser uno de: {', '.join(TIPOS_ACTIVIDAD)}")
        return v
    
    @field_validator('localidad')
    @classmethod
    def validate_localidad(cls, v):
        if v is not None and v not in LOCALIDADES:
            raise ValueError(f"Localidad debe ser una de: {', '.join(LOCALIDADES)}")
        return v
    
    @field_validator('nivel_actividad')
    @classmethod
    def validate_nivel_actividad(cls, v):
        if v is not None and v not in NIVELES_ACTIVIDAD:
            raise ValueError(f"Nivel de actividad debe ser uno de: {', '.join(NIVELES_ACTIVIDAD)}")
        return v
    
    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        if v is not None and v not in ESTADOS:
            raise ValueError(f"Estado debe ser uno de: {', '.join(ESTADOS)}")
        return v
    
    def to_db_dict(self, exclude_unset: bool = False):
        """Convert to dict for database, converting HttpUrl to str."""
        data = self.model_dump(exclude_unset=exclude_unset)
        if data.get('enlace_externo'):
            data['enlace_externo'] = str(data['enlace_externo'])
        if data.get('imagen_url'):
            data['imagen_url'] = str(data['imagen_url'])
        return data


class ActividadResponse(ActividadBase):
    """Schema for Activity response (RF-006, RF-007)."""
    id: UUID
    fuente: str
    estado: str
    popularidad_favoritos: int
    popularidad_vistas: Decimal
    popularidad_normalizada: Decimal
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ActividadListItem(BaseModel):
    """Simplified schema for activity list (RF-006)."""
    id: UUID
    titulo: str
    descripcion_corta: str = Field(..., description="First 200 characters of descripcion")
    imagen_url: Optional[str]
    fecha_inicio: datetime
    localidad: str
    tipo: str
    precio: Decimal
    es_gratis: bool
    etiquetas: List[str]
    popularidad_normalizada: Decimal
    
    class Config:
        from_attributes = True


class PaginationMetadata(BaseModel):
    """Pagination metadata for list responses (RF-006)."""
    total: int
    page: int
    page_size: int
    total_pages: int


class ActividadListResponse(BaseModel):
    """Response schema for paginated activity list (RF-006)."""
    data: List[ActividadListItem]
    pagination: PaginationMetadata


class ActividadSearchQuery(BaseModel):
    """Query parameters for activity search and filters (RF-006, RF-008)."""
    # Search
    q: Optional[str] = Field(None, description="Search query")
    
    # Filters
    tipo: Optional[str] = None
    localidad: Optional[str] = None
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None
    precio_min: Optional[Decimal] = Field(None, ge=0)
    precio_max: Optional[Decimal] = Field(None, ge=0)
    es_gratis: Optional[bool] = None
    nivel_actividad: Optional[str] = None
    etiquetas: Optional[List[str]] = None
    
    # Pagination
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    
    # Sorting
    sort_by: str = Field(default="fecha_inicio", description="Field to sort by")
    sort_order: str = Field(default="asc", description="asc or desc")
    
    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        if v is not None and v not in TIPOS_ACTIVIDAD:
            raise ValueError(f"Tipo debe ser uno de: {', '.join(TIPOS_ACTIVIDAD)}")
        return v
    
    @field_validator('localidad')
    @classmethod
    def validate_localidad(cls, v):
        if v is not None and v not in LOCALIDADES:
            raise ValueError(f"Localidad debe ser una de: {', '.join(LOCALIDADES)}")
        return v
    
    @field_validator('sort_order')
    @classmethod
    def validate_sort_order(cls, v):
        if v not in ["asc", "desc"]:
            raise ValueError("sort_order debe ser 'asc' o 'desc'")
        return v


class ImportResult(BaseModel):
    """Result schema for CSV/JSON import (RF-010)."""
    total_procesados: int
    exitosos: int
    duplicados: int
    errores: int
    errores_detalle: List[dict] = []


class ActividadEstadoUpdate(BaseModel):
    """Schema for updating activity status (RF-018)."""
    estado: str
    nota: Optional[str] = Field(None, max_length=500, description="Nota de aprobación o rechazo")
    
    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v):
        if v not in ["activa", "rechazada"]:
            raise ValueError("Estado debe ser 'activa' o 'rechazada' para validación")
        return v
