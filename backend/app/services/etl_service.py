"""
ETL Service for running ETL pipeline directly from backend.
This service adapts the ETL pipeline to work with backend models.
"""
import asyncio
import csv
import logging
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import re

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.activity import Actividad
from app.models.etl_execution import ETLExecution, ETLStatus
from app.schemas.activity import ActividadCreate
from app.core.config import settings


logger = logging.getLogger(__name__)


class ETLService:
    """Service for running ETL pipeline from backend."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def run_csv_etl(
        self,
        execution_id: int,
        file_path: str
    ) -> Dict[str, Any]:
        """
        Run ETL pipeline for CSV file.
        
        Args:
            execution_id: ETL execution ID to track
            file_path: Path to CSV file
            
        Returns:
            Dict with execution statistics
        """
        execution = await self._get_execution(execution_id)
        if not execution:
            raise ValueError(f"ETL execution {execution_id} not found")
        
        # Update status to running
        execution.status = ETLStatus.RUNNING
        execution.started_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(execution)  # Refresh to ensure we have latest state
        
        stats = {
            'extracted': 0,
            'cleaned': 0,
            'valid': 0,
            'invalid': 0,
            'normalized': 0,
            'loaded': 0,
            'failed': 0,
            'errors': []
        }
        
        try:
            # 1. Extract
            records = await self._extract_csv(file_path)
            stats['extracted'] = len(records)
            
            if not records:
                logger.warning("No records extracted")
                execution.status = ETLStatus.FAILED
                execution.error_message = "No records extracted from CSV"
                execution.finished_at = datetime.utcnow()
                await self.db.commit()
                return stats
            
            # 2. Transform - Clean
            records = await self._clean_records(records)
            stats['cleaned'] = len(records)
            
            # 3. Transform - Validate and Normalize
            valid_records, invalid_records = await self._validate_and_normalize(records)
            stats['valid'] = len(valid_records)
            stats['invalid'] = len(invalid_records)
            stats['normalized'] = len(valid_records)
            
            if invalid_records:
                stats['errors'].extend([err.get('error', 'Unknown error') for err in invalid_records])
            
            if not valid_records:
                logger.error("No valid records after validation")
                execution.status = ETLStatus.FAILED
                execution.error_message = "No valid records after validation"
                execution.finished_at = datetime.utcnow()
                await self.db.commit()
                return stats
            
            # 4. Load
            loaded, failed, errors = await self._load_records(valid_records)
            stats['loaded'] = loaded
            stats['failed'] = failed
            stats['errors'].extend(errors)
            
            # Update execution with results
            execution.status = ETLStatus.SUCCESS if failed == 0 else ETLStatus.SUCCESS
            execution.records_extracted = stats['extracted']
            execution.records_transformed = stats['normalized']
            execution.records_loaded = stats['loaded']
            execution.records_failed = stats['failed']
            execution.finished_at = datetime.utcnow()
            
            if stats['errors']:
                error_summary = f"{len(stats['errors'])} errors occurred."
                if stats['errors']:
                    error_summary += f" First: {stats['errors'][0][:200]}"
                execution.error_message = error_summary
            
            await self.db.commit()
            
            # Log detailed summary
            logger.info("=" * 60)
            logger.info(f"ETL execution {execution_id} completed!")
            logger.info(f"  Extracted: {stats['extracted']}")
            logger.info(f"  Cleaned: {stats['cleaned']}")
            logger.info(f"  Valid: {stats['valid']}")
            logger.info(f"  Invalid: {stats['invalid']}")
            logger.info(f"  Normalized: {stats['normalized']}")
            logger.info(f"  Loaded: {stats['loaded']}")
            logger.info(f"  Failed: {stats['failed']}")
            if stats['errors']:
                logger.warning(f"  Errors: {len(stats['errors'])}")
                for i, err in enumerate(stats['errors'][:5], 1):
                    logger.warning(f"    {i}. {err[:100]}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}", exc_info=True)
            stats['errors'].append(str(e))
            
            # Try to update execution status to failed
            try:
                # Refresh execution to ensure it's still attached to session
                await self.db.refresh(execution)
                execution.status = ETLStatus.FAILED
                execution.error_message = str(e)[:500]
                execution.finished_at = datetime.utcnow()
                await self.db.commit()
            except Exception as update_error:
                logger.error(f"Failed to update ETL execution status: {update_error}", exc_info=True)
                # If we can't update, try to get a fresh execution object
                try:
                    fresh_execution = await self._get_execution(execution_id)
                    if fresh_execution:
                        fresh_execution.status = ETLStatus.FAILED
                        fresh_execution.error_message = str(e)[:500]
                        fresh_execution.finished_at = datetime.utcnow()
                        await self.db.commit()
                except Exception as final_error:
                    logger.error(f"Failed to update ETL execution with fresh object: {final_error}", exc_info=True)
        
        return stats
    
    async def _get_execution(self, execution_id: int) -> Optional[ETLExecution]:
        """Get ETL execution by ID."""
        result = await self.db.execute(
            select(ETLExecution).where(ETLExecution.id == execution_id)
        )
        return result.scalar_one_or_none()
    
    async def _extract_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract records from CSV file."""
        logger.info(f"Extracting from CSV: {file_path}")
        
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        records = []
        with open(file_path_obj, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))
        
        logger.info(f"Extracted {len(records)} records from CSV")
        return records
    
    async def _clean_records(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean and sanitize records."""
        logger.info(f"Cleaning {len(records)} records")
        
        cleaned = []
        for record in records:
            try:
                cleaned_record = {}
                for key, value in record.items():
                    if value is None:
                        cleaned_record[key] = None
                        continue
                    
                    if isinstance(value, str):
                        # Remove extra whitespace
                        value = re.sub(r'\s+', ' ', value.strip())
                        # Remove special characters from beginning/end
                        value = value.strip('.,;:')
                        # Convert empty strings to None
                        if not value:
                            value = None
                    
                    cleaned_record[key] = value
                
                cleaned.append(cleaned_record)
            except Exception as e:
                logger.warning(f"Error cleaning record: {e}")
                continue
        
        logger.info(f"Cleaned {len(cleaned)}/{len(records)} records")
        return cleaned
    
    async def _validate_and_normalize(
        self,
        records: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Validate and normalize records, mapping ETL fields to backend model fields."""
        logger.info(f"Validating and normalizing {len(records)} records")
        
        valid = []
        invalid = []
        
        for i, record in enumerate(records):
            try:
                # Map ETL fields to backend model fields
                normalized = self._map_etl_to_backend_fields(record)
                logger.debug(f"Record {i} normalized: titulo={normalized.get('titulo')}, tipo={normalized.get('tipo')}")
                
                # Validate using backend schema
                validated = ActividadCreate(**normalized)
                valid.append(validated.model_dump())
                logger.debug(f"Record {i} validated successfully")
                
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Validation failed for record {i} (titulo={record.get('nombre', record.get('titulo', 'Unknown'))}): {error_msg}")
                logger.debug(f"Record {i} data: {record}")
                logger.debug(f"Normalized data (if available): {normalized if 'normalized' in locals() else 'N/A'}")
                invalid.append({
                    "record": record,
                    "error": error_msg
                })
        
        logger.info(f"Validation complete: {len(valid)} valid, {len(invalid)} invalid")
        if invalid:
            logger.warning(f"Invalid records details: {[err['error'] for err in invalid[:5]]}")  # Log first 5 errors
        
        return valid, invalid
    
    def _map_etl_to_backend_fields(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map ETL record fields to backend Actividad model fields.
        
        ETL fields -> Backend fields:
        - nombre -> titulo
        - direccion -> ubicacion_direccion
        - es_gratuita -> es_gratis
        - contacto_telefono, contacto_email, contacto_web -> contacto (combined)
        - fecha_inicio, fecha_fin -> convert date to datetime
        """
        mapped = {}
        
        # Map titulo
        mapped['titulo'] = record.get('nombre') or record.get('titulo', '')
        
        # Map descripcion
        mapped['descripcion'] = record.get('descripcion', '')
        
        # Map tipo (normalize to lowercase)
        tipo = record.get('tipo', '').lower()
        tipo_map = {
            'deporte': 'deporte',
            'deportivo': 'deporte',
            'deportiva': 'deporte',
            'cultura': 'cultura',
            'cultural': 'cultura',
            'recreacion': 'recreacion',
            'recreación': 'recreacion',
            'recreativo': 'recreacion',
            'recreativa': 'recreacion',
        }
        mapped['tipo'] = tipo_map.get(tipo, tipo if tipo in ['cultura', 'deporte', 'recreacion'] else 'cultura')
        
        # Map fechas (convert date to datetime with timezone)
        fecha_inicio = record.get('fecha_inicio')
        if fecha_inicio:
            if isinstance(fecha_inicio, str):
                fecha_inicio = self._parse_date(fecha_inicio)
            if isinstance(fecha_inicio, datetime):
                # Ensure timezone-aware
                if fecha_inicio.tzinfo is None:
                    fecha_inicio = fecha_inicio.replace(tzinfo=timezone.utc)
                mapped['fecha_inicio'] = fecha_inicio
            elif fecha_inicio:
                dt = datetime.combine(fecha_inicio, datetime.min.time())
                mapped['fecha_inicio'] = dt.replace(tzinfo=timezone.utc)
        else:
            # Default to now if not provided
            mapped['fecha_inicio'] = datetime.now(timezone.utc)
        
        fecha_fin = record.get('fecha_fin')
        if fecha_fin:
            if isinstance(fecha_fin, str):
                fecha_fin = self._parse_date(fecha_fin)
            if isinstance(fecha_fin, datetime):
                # Ensure timezone-aware
                if fecha_fin.tzinfo is None:
                    fecha_fin = fecha_fin.replace(tzinfo=timezone.utc)
                mapped['fecha_fin'] = fecha_fin
            elif fecha_fin:
                dt = datetime.combine(fecha_fin, datetime.min.time())
                mapped['fecha_fin'] = dt.replace(tzinfo=timezone.utc)
        else:
            mapped['fecha_fin'] = None
        
        # Map ubicacion
        mapped['ubicacion_direccion'] = record.get('direccion') or record.get('ubicacion_direccion', '')
        
        # Map coordinates
        lat = record.get('ubicacion_lat') or record.get('lat')
        lng = record.get('ubicacion_lng') or record.get('lng') or record.get('lon')
        
        if lat:
            try:
                mapped['ubicacion_lat'] = Decimal(str(lat))
            except:
                mapped['ubicacion_lat'] = Decimal('4.6097')  # Bogotá default
        else:
            mapped['ubicacion_lat'] = Decimal('4.6097')
        
        if lng:
            try:
                mapped['ubicacion_lng'] = Decimal(str(lng))
            except:
                mapped['ubicacion_lng'] = Decimal('-74.0817')  # Bogotá default
        else:
            mapped['ubicacion_lng'] = Decimal('-74.0817')
        
        # Map localidad (normalize)
        localidad = record.get('localidad', '')
        localidades_validas = ['Chapinero', 'Santa Fe', 'La Candelaria']
        localidad_normalized = None
        
        for loc in localidades_validas:
            if loc.lower() in localidad.lower():
                localidad_normalized = loc
                break
        
        mapped['localidad'] = localidad_normalized or 'Chapinero'  # Default
        
        # Map precio
        precio = record.get('precio', 0)
        try:
            mapped['precio'] = Decimal(str(precio))
        except:
            mapped['precio'] = Decimal('0')
        
        # Map es_gratis
        es_gratuita = record.get('es_gratuita') or record.get('es_gratis')
        if isinstance(es_gratuita, str):
            mapped['es_gratis'] = es_gratuita.lower() in ('true', '1', 'si', 'sí', 'yes')
        else:
            mapped['es_gratis'] = bool(es_gratuita) if es_gratuita is not None else (mapped['precio'] == 0)
        
        # Map nivel_actividad
        nivel = record.get('nivel_actividad')
        if nivel:
            nivel_lower = nivel.lower()
            if nivel_lower in ['bajo', 'medio', 'alto']:
                mapped['nivel_actividad'] = nivel_lower
            else:
                mapped['nivel_actividad'] = None
        else:
            mapped['nivel_actividad'] = None
        
        # Map etiquetas
        etiquetas = record.get('etiquetas', [])
        if isinstance(etiquetas, str):
            # Remove quotes if present
            etiquetas = etiquetas.strip('"\'')
            # Split by comma or semicolon
            etiquetas = [tag.strip() for tag in re.split(r'[,;]', etiquetas) if tag.strip()]
        elif not isinstance(etiquetas, list):
            etiquetas = []
        
        # Ensure we have at least one tag (required by schema)
        if not etiquetas:
            # Try to generate tags from tipo
            tipo_tag = mapped.get('tipo', 'cultura')
            etiquetas = [tipo_tag]
            logger.debug(f"No etiquetas found, using tipo as tag: {tipo_tag}")
        
        mapped['etiquetas'] = [tag.lower().strip() for tag in etiquetas if tag]
        
        # Map contacto (combine phone, email, web)
        contacto_parts = []
        if record.get('contacto_telefono'):
            contacto_parts.append(f"Tel: {record['contacto_telefono']}")
        if record.get('contacto_email'):
            contacto_parts.append(f"Email: {record['contacto_email']}")
        if record.get('contacto_web') or record.get('enlace_externo'):
            contacto_parts.append(f"Web: {record.get('contacto_web') or record.get('enlace_externo')}")
        
        mapped['contacto'] = ' | '.join(contacto_parts) if contacto_parts else None
        mapped['enlace_externo'] = record.get('contacto_web') or record.get('enlace_externo')
        mapped['imagen_url'] = record.get('imagen_url')
        
        # Set fuente and estado for imported activities
        mapped['fuente'] = record.get('fuente', 'csv')
        mapped['estado'] = 'pendiente_validacion'  # Requires admin approval
        
        return mapped
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime (timezone-aware)."""
        if not date_str:
            return None
        
        date_str = date_str.strip()
        
        # Try common formats
        formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%d-%m-%Y',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S%z',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                # Ensure timezone-aware
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_str}")
        return None
    
    async def _load_records(
        self,
        records: List[Dict[str, Any]]
    ) -> Tuple[int, int, List[str]]:
        """Load validated records into database."""
        logger.info(f"Loading {len(records)} records to database")
        
        loaded = 0
        failed = 0
        errors = []
        
        for idx, record in enumerate(records):
            try:
                logger.debug(f"Loading record {idx+1}/{len(records)}: {record.get('titulo', 'Unknown')}")
                
                # Check for duplicates (titulo + fecha_inicio + ubicacion_direccion)
                duplicate_query = select(Actividad).where(
                    and_(
                        Actividad.titulo == record['titulo'],
                        Actividad.fecha_inicio == record['fecha_inicio'],
                        Actividad.ubicacion_direccion == record['ubicacion_direccion'],
                    )
                )
                result = await self.db.execute(duplicate_query)
                existing = result.scalar_one_or_none()
                
                if existing:
                    logger.info(f"Skipping duplicate: {record['titulo']} (ID: {existing.id})")
                    continue
                
                # Create activity with all required fields
                activity = Actividad(
                    titulo=record['titulo'],
                    descripcion=record['descripcion'],
                    tipo=record['tipo'],
                    fecha_inicio=record['fecha_inicio'],
                    fecha_fin=record.get('fecha_fin'),
                    ubicacion_direccion=record['ubicacion_direccion'],
                    ubicacion_lat=record['ubicacion_lat'],
                    ubicacion_lng=record['ubicacion_lng'],
                    localidad=record['localidad'],
                    precio=record['precio'],
                    es_gratis=record['es_gratis'],
                    nivel_actividad=record.get('nivel_actividad'),
                    etiquetas=record['etiquetas'],
                    contacto=record.get('contacto'),
                    enlace_externo=record.get('enlace_externo'),
                    imagen_url=record.get('imagen_url'),
                    fuente=record.get('fuente', 'csv'),
                    estado=record.get('estado', 'pendiente_validacion'),
                    popularidad_favoritos=0,
                    popularidad_vistas=Decimal('0'),
                    popularidad_normalizada=Decimal('0'),
                )
                self.db.add(activity)
                await self.db.commit()
                loaded += 1
                logger.debug(f"Successfully loaded activity: {activity.titulo} (ID: {activity.id})")
                
            except Exception as e:
                failed += 1
                error_msg = f"Failed to load '{record.get('titulo', 'Unknown')}': {str(e)}"
                logger.error(error_msg, exc_info=True)
                logger.debug(f"Failed record data: {record}")
                errors.append(error_msg)
                await self.db.rollback()
                continue
        
        logger.info(f"Loading complete: {loaded} loaded, {failed} failed")
        if errors:
            logger.warning(f"Load errors: {errors[:5]}")  # Log first 5 errors
        
        return loaded, failed, errors

