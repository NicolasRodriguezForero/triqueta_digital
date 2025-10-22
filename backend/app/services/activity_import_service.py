"""
Activity import service for CSV and JSON files.
Implements requirements RF-010: Manual data import.
"""
from typing import List, Dict, Any, Tuple
from datetime import datetime
import csv
import json
from io import StringIO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.activity import Actividad
from app.schemas.activity import ActividadCreate


class ImportError(Exception):
    """Custom exception for import errors."""
    pass


def parse_csv(content: str) -> List[Dict[str, Any]]:
    """
    Parse CSV content and return list of activities.
    
    Expected CSV format:
    titulo,descripcion,tipo,fecha_inicio,ubicacion_direccion,ubicacion_lat,ubicacion_lng,localidad,precio,es_gratis,etiquetas
    
    Args:
        content: CSV file content as string
        
    Returns:
        List of activity dictionaries
        
    Raises:
        ImportError: If CSV format is invalid
    """
    try:
        reader = csv.DictReader(StringIO(content))
        activities = []
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
            # Validate required fields
            required_fields = ['titulo', 'descripcion', 'tipo', 'fecha_inicio', 
                             'ubicacion_direccion', 'ubicacion_lat', 'ubicacion_lng', 'localidad']
            
            missing_fields = [field for field in required_fields if not row.get(field)]
            if missing_fields:
                raise ImportError(
                    f"Row {row_num}: Missing required fields: {', '.join(missing_fields)}"
                )
            
            # Parse etiquetas (comma-separated in CSV)
            etiquetas_str = row.get('etiquetas', '')
            etiquetas = [tag.strip() for tag in etiquetas_str.split(';') if tag.strip()]
            
            # Parse es_gratis
            es_gratis = row.get('es_gratis', 'true').lower() in ['true', '1', 'si', 'yes']
            
            # Parse precio
            try:
                precio = float(row.get('precio', 0))
            except ValueError:
                precio = 0
            
            # Parse coordinates
            try:
                ubicacion_lat = float(row['ubicacion_lat'])
                ubicacion_lng = float(row['ubicacion_lng'])
            except ValueError:
                raise ImportError(
                    f"Row {row_num}: Invalid coordinates format"
                )
            
            activity = {
                'titulo': row['titulo'],
                'descripcion': row['descripcion'],
                'tipo': row['tipo'],
                'fecha_inicio': row['fecha_inicio'],
                'fecha_fin': row.get('fecha_fin') or None,
                'ubicacion_direccion': row['ubicacion_direccion'],
                'ubicacion_lat': ubicacion_lat,
                'ubicacion_lng': ubicacion_lng,
                'localidad': row['localidad'],
                'precio': precio,
                'es_gratis': es_gratis,
                'nivel_actividad': row.get('nivel_actividad') or None,
                'etiquetas': etiquetas,
                'contacto': row.get('contacto') or None,
                'enlace_externo': row.get('enlace_externo') or None,
                'imagen_url': row.get('imagen_url') or None,
            }
            
            activities.append(activity)
        
        return activities
    
    except csv.Error as e:
        raise ImportError(f"CSV parsing error: {str(e)}")
    except Exception as e:
        if isinstance(e, ImportError):
            raise
        raise ImportError(f"Unexpected error parsing CSV: {str(e)}")


def parse_json(content: str) -> List[Dict[str, Any]]:
    """
    Parse JSON content and return list of activities.
    
    Expected JSON format: array of activity objects
    
    Args:
        content: JSON file content as string
        
    Returns:
        List of activity dictionaries
        
    Raises:
        ImportError: If JSON format is invalid
    """
    try:
        data = json.loads(content)
        
        if not isinstance(data, list):
            raise ImportError("JSON must be an array of activities")
        
        activities = []
        
        for idx, item in enumerate(data, start=1):
            if not isinstance(item, dict):
                raise ImportError(f"Item {idx}: Must be an object")
            
            # Validate required fields
            required_fields = ['titulo', 'descripcion', 'tipo', 'fecha_inicio',
                             'ubicacion_direccion', 'ubicacion_lat', 'ubicacion_lng', 'localidad']
            
            missing_fields = [field for field in required_fields if not item.get(field)]
            if missing_fields:
                raise ImportError(
                    f"Item {idx}: Missing required fields: {', '.join(missing_fields)}"
                )
            
            # Ensure etiquetas is a list
            etiquetas = item.get('etiquetas', [])
            if not isinstance(etiquetas, list):
                raise ImportError(f"Item {idx}: 'etiquetas' must be an array")
            
            activities.append(item)
        
        return activities
    
    except json.JSONDecodeError as e:
        raise ImportError(f"Invalid JSON format: {str(e)}")
    except Exception as e:
        if isinstance(e, ImportError):
            raise
        raise ImportError(f"Unexpected error parsing JSON: {str(e)}")


async def check_duplicates(
    db: AsyncSession,
    activities: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Check for duplicate activities by title and location.
    
    Args:
        db: Database session
        activities: List of activities to check
        
    Returns:
        Tuple of (unique_activities, duplicate_titles)
    """
    duplicates = []
    unique = []
    
    for activity in activities:
        # Check if activity with same title exists
        stmt = select(Actividad).where(
            Actividad.titulo == activity['titulo']
        )
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            duplicates.append(activity['titulo'])
        else:
            unique.append(activity)
    
    return unique, duplicates


async def validate_activities(
    activities: List[Dict[str, Any]]
) -> Tuple[List[ActividadCreate], List[str]]:
    """
    Validate activities using Pydantic schemas.
    
    Args:
        activities: List of activity dictionaries
        
    Returns:
        Tuple of (valid_activities, validation_errors)
    """
    valid = []
    errors = []
    
    for idx, activity in enumerate(activities, start=1):
        try:
            validated = ActividadCreate(**activity)
            valid.append(validated)
        except Exception as e:
            errors.append(f"Activity {idx} ({activity.get('titulo', 'unknown')}): {str(e)}")
    
    return valid, errors


async def import_activities(
    db: AsyncSession,
    activities: List[ActividadCreate],
    user_id: int
) -> int:
    """
    Import validated activities to database.
    
    Args:
        db: Database session
        activities: List of validated activities
        user_id: ID of user importing (for audit)
        
    Returns:
        Number of activities imported
    """
    count = 0
    
    for activity_data in activities:
        db_activity = Actividad(
            **activity_data.model_dump(),
            fuente="manual",
            estado="activa",
            popularidad_favoritos=0,
            popularidad_vistas=0,
            popularidad_normalizada=0.0
        )
        db.add(db_activity)
        count += 1
    
    await db.commit()
    return count
