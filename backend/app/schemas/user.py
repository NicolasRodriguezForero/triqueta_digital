"""
User schemas for request/response validation.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class PerfilUsuarioBase(BaseModel):
    """Base schema for user profile."""
    nombre_completo: Optional[str] = Field(None, max_length=255)
    telefono: Optional[str] = Field(None, max_length=20)
    biografia: Optional[str] = None
    etiquetas_interes: List[str] = Field(default_factory=list)
    localidad_preferida: Optional[str] = Field(None, max_length=100)
    disponibilidad_horaria: Optional[str] = Field(None, max_length=50)
    nivel_actividad: Optional[str] = Field(None, max_length=20)


class PerfilUsuarioCreate(PerfilUsuarioBase):
    """Schema for creating user profile."""
    pass


class PerfilUsuarioUpdate(BaseModel):
    """Schema for updating user profile (all fields optional)."""
    nombre_completo: Optional[str] = Field(None, max_length=255)
    telefono: Optional[str] = Field(None, max_length=20)
    biografia: Optional[str] = None
    etiquetas_interes: Optional[List[str]] = None
    localidad_preferida: Optional[str] = Field(None, max_length=100)
    disponibilidad_horaria: Optional[str] = Field(None, max_length=50)
    nivel_actividad: Optional[str] = Field(None, max_length=20)


class PerfilUsuarioResponse(PerfilUsuarioBase):
    """Schema for user profile response."""
    id: int
    usuario_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UsuarioBase(BaseModel):
    """Base schema for user."""
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    """Schema for creating user."""
    password: str = Field(..., min_length=8)


class UsuarioUpdate(BaseModel):
    """Schema for updating user (all fields optional)."""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    """Schema for user response (without sensitive data)."""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    perfil: Optional[PerfilUsuarioResponse] = None
    
    class Config:
        from_attributes = True


class UsuarioWithProfile(UsuarioResponse):
    """Schema for user with profile data."""
    pass
