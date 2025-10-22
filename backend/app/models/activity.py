"""
Activity models for cultural and recreational activities.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL, Boolean, ARRAY, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base


class Actividad(Base):
    """
    Activity model for cultural, recreational and sports activities.
    
    Implements requirements RF-006 to RF-010 from SRS.
    
    Attributes:
        id: UUID primary key
        titulo: Activity title
        descripcion: Full activity description (supports markdown)
        tipo: Activity type (cultura, deporte, recreacion)
        fecha_inicio: Start datetime
        fecha_fin: End datetime (optional)
        ubicacion_direccion: Physical address
        ubicacion_lat: GPS latitude (DECIMAL for precision)
        ubicacion_lng: GPS longitude (DECIMAL for precision)
        localidad: Locality (Chapinero, Santa Fe, La Candelaria)
        precio: Price in COP (0 for free activities)
        es_gratis: Boolean flag for free activities
        nivel_actividad: Physical activity level (bajo, medio, alto)
        etiquetas: Array of tags for categorization and recommendations
        contacto: Contact information string
        enlace_externo: External URL (optional)
        fuente: Data source (manual, idrd, api, csv)
        estado: Activity status (activa, pendiente_validacion, rechazada, inactiva)
        popularidad_favoritos: Count of favorites (RF-015)
        popularidad_vistas: Weighted view count (RF-015)
        popularidad_normalizada: Normalized popularity score [0-1] (RF-015)
        imagen_url: Image URL (optional)
        created_at: Creation timestamp
        updated_at: Last update timestamp
        favoritos: Relationship to Favorito
    """
    __tablename__ = "actividades"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic information
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)  # cultura, deporte, recreacion
    
    # Timing
    fecha_inicio = Column(DateTime(timezone=True), nullable=False)
    fecha_fin = Column(DateTime(timezone=True), nullable=True)
    
    # Location
    ubicacion_direccion = Column(String(500), nullable=False)
    ubicacion_lat = Column(DECIMAL(10, 8), nullable=False)
    ubicacion_lng = Column(DECIMAL(11, 8), nullable=False)
    localidad = Column(String(100), nullable=False)
    
    # Pricing
    precio = Column(DECIMAL(10, 2), default=0, nullable=False)
    es_gratis = Column(Boolean, default=True, nullable=False)
    
    # Details
    nivel_actividad = Column(String(50), nullable=True)  # bajo, medio, alto
    etiquetas = Column(ARRAY(String), nullable=False)
    contacto = Column(String(255), nullable=True)
    enlace_externo = Column(String(500), nullable=True)
    imagen_url = Column(String(500), nullable=True)
    
    # Data management
    fuente = Column(String(100), default="manual", nullable=False)
    estado = Column(String(50), default="activa", nullable=False)
    
    # Popularity metrics (RF-015)
    popularidad_favoritos = Column(Integer, default=0, nullable=False)
    popularidad_vistas = Column(DECIMAL(10, 2), default=0, nullable=False)
    popularidad_normalizada = Column(DECIMAL(5, 4), default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    favoritos = relationship("Favorito", back_populates="actividad", cascade="all, delete-orphan")
    
    # Indexes for performance (RF-006, RF-008)
    __table_args__ = (
        Index("idx_actividades_localidad", "localidad"),
        Index("idx_actividades_tipo", "tipo"),
        Index("idx_actividades_fecha_inicio", "fecha_inicio"),
        Index("idx_actividades_estado", "estado"),
        Index("idx_actividades_etiquetas", "etiquetas", postgresql_using="gin"),
        Index("idx_actividades_popularidad", "popularidad_normalizada"),
    )
