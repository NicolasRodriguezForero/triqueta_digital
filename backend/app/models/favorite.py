"""
Favorite model for user-activity relationships.
"""
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class Favorito(Base):
    """
    Favorite model to track user's favorite activities.
    
    Attributes:
        id: Primary key
        usuario_id: Foreign key to Usuario
        actividad_id: Foreign key to Actividad
        usuario: Relationship to Usuario
        actividad: Relationship to Actividad
    """
    __tablename__ = "favoritos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    actividad_id = Column(Integer, ForeignKey("actividades.id"), nullable=False, index=True)
    
    # Relationships
    usuario = relationship("Usuario", back_populates="favoritos")
    actividad = relationship("Actividad", back_populates="favoritos")
    
    # Unique constraint to prevent duplicate favorites
    __table_args__ = (
        UniqueConstraint("usuario_id", "actividad_id", name="uq_usuario_actividad"),
    )
