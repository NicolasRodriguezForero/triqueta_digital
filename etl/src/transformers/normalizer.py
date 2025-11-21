"""
Data normalizer for standardizing field values.
"""
from typing import List, Dict, Any, Set
import logging
from datetime import datetime
import hashlib
import json


class DataNormalizer:
    """Normalize and standardize data."""
    
    # Standardized values
    LOCALIDADES_VALIDAS = {"Chapinero", "Santa Fe", "La Candelaria"}
    TIPOS_ACTIVIDAD = {"Cultura", "Deporte", "Recreación", "Educación"}
    
    def __init__(self, logger: logging.Logger = None):
        """
        Initialize normalizer.
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.seen_hashes: Set[str] = set()
    
    async def normalize(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize records and remove duplicates.
        
        Args:
            records: Records to normalize
            
        Returns:
            Normalized and deduplicated records
        """
        self.logger.info(f"Normalizing {len(records)} records")
        
        normalized = []
        duplicates = 0
        
        for record in records:
            try:
                # Detect duplicates
                record_hash = self._hash_record(record)
                if record_hash in self.seen_hashes:
                    duplicates += 1
                    self.logger.debug(f"Duplicate detected: {record.get('nombre', 'Unknown')}")
                    continue
                
                self.seen_hashes.add(record_hash)
                
                # Normalize record
                normalized_record = self._normalize_record(record)
                normalized.append(normalized_record)
                
            except Exception as e:
                self.logger.error(f"Error normalizing record: {e}")
                continue
        
        self.logger.info(f"Normalization complete: {len(normalized)} unique records, {duplicates} duplicates removed")
        return normalized
    
    def _normalize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize individual record.
        
        Args:
            record: Record to normalize
            
        Returns:
            Normalized record
        """
        normalized = record.copy()
        
        # Normalize localidad
        if 'localidad' in normalized and normalized['localidad']:
            normalized['localidad'] = self._normalize_localidad(normalized['localidad'])
        
        # Normalize tipo
        if 'tipo' in normalized and normalized['tipo']:
            normalized['tipo'] = self._normalize_tipo(normalized['tipo'])
        
        # Normalize etiquetas
        if 'etiquetas' in normalized and normalized['etiquetas']:
            normalized['etiquetas'] = self._normalize_tags(normalized['etiquetas'])
        
        # Ensure boolean for es_gratuita
        if 'es_gratuita' in normalized:
            if isinstance(normalized['es_gratuita'], str):
                normalized['es_gratuita'] = normalized['es_gratuita'].lower() in ('true', 'sí', 'si', '1', 'yes')
            elif normalized.get('precio', 0) == 0:
                normalized['es_gratuita'] = True
        
        # Normalize dates
        for date_field in ['fecha_inicio', 'fecha_fin']:
            if date_field in normalized and normalized[date_field]:
                if isinstance(normalized[date_field], str):
                    try:
                        # Try parsing common formats
                        normalized[date_field] = datetime.strptime(
                            normalized[date_field], '%Y-%m-%d'
                        ).date()
                    except ValueError:
                        try:
                            normalized[date_field] = datetime.strptime(
                                normalized[date_field], '%d/%m/%Y'
                            ).date()
                        except ValueError:
                            self.logger.warning(f"Could not parse date: {normalized[date_field]}")
                            normalized[date_field] = None
        
        return normalized
    
    def _normalize_localidad(self, localidad: str) -> str:
        """Normalize localidad to standard values."""
        localidad_lower = localidad.lower()
        
        for valid in self.LOCALIDADES_VALIDAS:
            if valid.lower() in localidad_lower:
                return valid
        
        # Return as-is if no match (will be filtered later if needed)
        return localidad
    
    def _normalize_tipo(self, tipo: str) -> str:
        """Normalize tipo to standard values."""
        tipo_lower = tipo.lower()
        
        # Mapping common variations
        tipo_map = {
            'deporte': 'Deporte',
            'deportivo': 'Deporte',
            'deportiva': 'Deporte',
            'cultura': 'Cultura',
            'cultural': 'Cultura',
            'recreacion': 'Recreación',
            'recreativo': 'Recreación',
            'recreativa': 'Recreación',
            'educacion': 'Educación',
            'educativo': 'Educación',
            'educativa': 'Educación',
        }
        
        for key, value in tipo_map.items():
            if key in tipo_lower:
                return value
        
        return tipo.capitalize()
    
    def _normalize_tags(self, tags: List[str]) -> List[str]:
        """Normalize tags to lowercase and remove duplicates."""
        if not tags:
            return []
        
        normalized = []
        seen = set()
        
        for tag in tags:
            tag_lower = tag.lower().strip()
            if tag_lower and tag_lower not in seen:
                normalized.append(tag_lower)
                seen.add(tag_lower)
        
        return normalized
    
    def _hash_record(self, record: Dict[str, Any]) -> str:
        """
        Create hash of record for duplicate detection.
        
        Args:
            record: Record to hash
            
        Returns:
            Hash string
        """
        # Use key fields for hashing
        key_fields = {
            'nombre': record.get('nombre', ''),
            'localidad': record.get('localidad', ''),
            'fecha_inicio': str(record.get('fecha_inicio', '')),
        }
        
        # Create deterministic hash
        record_str = json.dumps(key_fields, sort_keys=True)
        return hashlib.md5(record_str.encode()).hexdigest()
