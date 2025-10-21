"""
User models for authentication and profile management.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY, DateTime, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Usuario(Base):
    """
    Usuario model for authentication.
    
    Attributes:
        id: Primary key
        email: Unique email address
        hashed_password: Bcrypt hashed password
        is_active: Account active status
        is_admin: Admin privileges flag
        perfil: Relationship to PerfilUsuario
        refresh_tokens: Relationship to RefreshToken
    """
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    perfil = relationship("PerfilUsuario", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="usuario", cascade="all, delete-orphan")
    favoritos = relationship("Favorito", back_populates="usuario", cascade="all, delete-orphan")


class PerfilUsuario(Base):
    """
    User profile model with preferences and personal information.
    
    Attributes:
        id: Primary key
        usuario_id: Foreign key to Usuario
        nombre_completo: User's full name
        telefono: Optional phone number
        etiquetas_interes: Array of interest tags for recommendations
        localidad_preferida: Preferred locality (Chapinero, Santa Fe, La Candelaria)
        disponibilidad_horaria: Preferred time availability
        nivel_actividad: Activity level preference (bajo, medio, alto)
        biografia: Optional user biography
        usuario: Relationship to Usuario
    """
    __tablename__ = "perfiles_usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    
    # Personal information
    nombre_completo = Column(String(255), nullable=True)
    telefono = Column(String(20), nullable=True)
    biografia = Column(Text, nullable=True)
    
    # Preferences for recommendations
    etiquetas_interes = Column(ARRAY(String), default=list, nullable=False)
    localidad_preferida = Column(String(100), nullable=True)  # Chapinero, Santa Fe, La Candelaria
    disponibilidad_horaria = Column(String(50), nullable=True)  # mañana, tarde, noche, fin_de_semana
    nivel_actividad = Column(String(20), nullable=True)  # bajo, medio, alto
    
    # Relationship
    usuario = relationship("Usuario", back_populates="perfil")


class RefreshToken(Base):
    """
    Refresh token model for JWT token management.
    
    Attributes:
        id: Primary key
        usuario_id: Foreign key to Usuario
        token: Unique refresh token string
        expires_at: Token expiration datetime
        revoked: Token revocation status
        usuario: Relationship to Usuario
    """
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    token = Column(String(500), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    
    # Relationship
    usuario = relationship("Usuario", back_populates="refresh_tokens")
