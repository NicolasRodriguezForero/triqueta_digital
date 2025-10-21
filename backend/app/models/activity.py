"""
Activity models for cultural and recreational activities.
"""
from datetime import date, time
from sqlalchemy import Column, Integer, String, Text, Date, Time, Float, Boolean, ARRAY, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class TipoActividad(str, enum.Enum):
    """Activity type enumeration."""
    CULTURAL = "cultural"
    DEPORTIVA = "deportiva"
    RECREATIVA = "recreativa"
    EDUCATIVA = "educativa"
    SOCIAL = "social"


class EstadoActividad(str, enum.Enum):
    """Activity status enumeration."""
    ACTIVA = "activa"
    PENDIENTE = "pendiente"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"


class Actividad(Base):
    """
    Activity model for cultural, recreational and sports activities.
    
    Attributes:
        id: Primary key
        titulo: Activity title
        descripcion: Activity description
        tipo: Activity type (cultural, deportiva, recreativa, etc.)
        localidad: Locality (Chapinero, Santa Fe, La Candelaria)
        direccion: Physical address
        latitud: GPS latitude
        longitud: GPS longitude
        fecha_inicio: Start date
        fecha_fin: End date (optional)
        hora_inicio: Start time
        hora_fin: End time
        precio: Price (0 for free activities)
        capacidad_maxima: Maximum capacity (optional)
        etiquetas: Array of tags for categorization
        estado: Activity status
        organizador: Organizer name
        contacto_email: Contact email
        contacto_telefono: Contact phone
        url_externa: External URL (optional)
        imagen_url: Image URL (optional)
        popularidad: Popularity score
        vistas: View count
        fuente: Data source (manual, idrd, api, etc.)
        validado: Validation status by admin
        favoritos: Relationship to Favorito
    """
    __tablename__ = "actividades"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic information
    titulo = Column(String(255), nullable=False, index=True)
    descripcion = Column(Text, nullable=False)
    tipo = Column(SQLEnum(TipoActividad), nullable=False, index=True)
    
    # Location
    localidad = Column(String(100), nullable=False, index=True)
    direccion = Column(String(500), nullable=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    
    # Timing
    fecha_inicio = Column(Date, nullable=False, index=True)
    fecha_fin = Column(Date, nullable=True)
    hora_inicio = Column(Time, nullable=True)
    hora_fin = Column(Time, nullable=True)
    
    # Details
    precio = Column(Float, default=0.0, nullable=False)
    capacidad_maxima = Column(Integer, nullable=True)
    etiquetas = Column(ARRAY(String), default=list, nullable=False, index=True)
    
    # Status
    estado = Column(SQLEnum(EstadoActividad), default=EstadoActividad.ACTIVA, nullable=False, index=True)
    
    # Contact
    organizador = Column(String(255), nullable=True)
    contacto_email = Column(String(255), nullable=True)
    contacto_telefono = Column(String(20), nullable=True)
    url_externa = Column(String(500), nullable=True)
    imagen_url = Column(String(500), nullable=True)
    
    # Metrics
    popularidad = Column(Float, default=0.0, nullable=False, index=True)
    vistas = Column(Integer, default=0, nullable=False)
    
    # Data management
    fuente = Column(String(50), nullable=False, default="manual")  # manual, idrd, api, csv
    validado = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    favoritos = relationship("Favorito", back_populates="actividad", cascade="all, delete-orphan")
