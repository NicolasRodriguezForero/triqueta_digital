"""
Data validator using Pydantic schemas.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import logging
from pydantic import BaseModel, Field, validator


class ActivitySchema(BaseModel):
    """Pydantic schema for activity validation."""
    
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: str = Field(..., min_length=1)
    tipo: str = Field(..., min_length=1, max_length=50)
    localidad: Optional[str] = Field(None, max_length=100)
    direccion: Optional[str] = Field(None, max_length=500)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    horario: Optional[str] = Field(None, max_length=255)
    precio: Optional[float] = Field(None, ge=0)
    es_gratuita: bool = True
    contacto_telefono: Optional[str] = Field(None, max_length=20)
    contacto_email: Optional[str] = Field(None, max_length=255)
    contacto_web: Optional[str] = Field(None, max_length=500)
    etiquetas: List[str] = Field(default_factory=list)
    fuente: str = Field(..., min_length=1, max_length=100)
    
    class Config:
        """Pydantic config."""
        str_strip_whitespace = True
        
    @validator('etiquetas', pre=True)
    def ensure_list(cls, v):
        """Ensure etiquetas is a list."""
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(',') if tag.strip()]
        return v or []
    
    @validator('precio')
    def validate_price(cls, v, values):
        """Validate price consistency with es_gratuita."""
        if values.get('es_gratuita') and v and v > 0:
            return 0.0
        return v


class DataValidator:
    """Validate and transform data using Pydantic."""
    
    def __init__(self, logger: logging.Logger = None):
        """
        Initialize validator.
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
    
    async def validate(self, records: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Validate records against schema.
        
        Args:
            records: Records to validate
            
        Returns:
            Tuple of (valid_records, invalid_records_with_errors)
        """
        self.logger.info(f"Validating {len(records)} records")
        
        valid = []
        invalid = []
        
        for i, record in enumerate(records):
            try:
                validated = ActivitySchema(**record)
                valid.append(validated.dict())
            except Exception as e:
                self.logger.warning(f"Validation failed for record {i}: {e}")
                invalid.append({
                    "record": record,
                    "error": str(e)
                })
        
        self.logger.info(f"Validation complete: {len(valid)} valid, {len(invalid)} invalid")
        return valid, invalid
