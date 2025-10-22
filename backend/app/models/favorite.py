"""
Favorite model for user-activity relationships.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base


class Favorito(Base):
    """
    Favorite model to track user's favorite activities.
    
    Implements requirements RF-011 to RF-013 from SRS.
    
    Attributes:
        id: UUID primary key
        usuario_id: Foreign key to Usuario (Integer for now, will migrate to UUID)
        actividad_id: Foreign key to Actividad (UUID)
        fecha_guardado: Timestamp when favorite was created
        usuario: Relationship to Usuario
        actividad: Relationship to Actividad
    """
    __tablename__ = "favoritos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    actividad_id = Column(UUID(as_uuid=True), ForeignKey("actividades.id"), nullable=False, index=True)
    
    # Timestamp
    fecha_guardado = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    
    # Relationships
    usuario = relationship("Usuario", back_populates="favoritos")
    actividad = relationship("Actividad", back_populates="favoritos")
    
    # Unique constraint to prevent duplicate favorites
    __table_args__ = (
        UniqueConstraint("usuario_id", "actividad_id", name="uq_usuario_actividad"),
    )
