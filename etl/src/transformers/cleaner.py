"""
Data cleaner for ETL transformation.
"""
from typing import List, Dict, Any
import re
import logging


class DataCleaner:
    """Clean and sanitize raw data."""
    
    def __init__(self, logger: logging.Logger = None):
        """
        Initialize cleaner.
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
    
    async def clean(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clean records.
        
        Args:
            records: Raw records to clean
            
        Returns:
            Cleaned records
        """
        self.logger.info(f"Cleaning {len(records)} records")
        
        cleaned = []
        for record in records:
            try:
                cleaned_record = self._clean_record(record)
                cleaned.append(cleaned_record)
            except Exception as e:
                self.logger.error(f"Error cleaning record: {e}")
                continue
        
        self.logger.info(f"Successfully cleaned {len(cleaned)}/{len(records)} records")
        return cleaned
    
    def _clean_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean individual record.
        
        Args:
            record: Raw record
            
        Returns:
            Cleaned record
        """
        cleaned = {}
        
        for key, value in record.items():
            # Skip None values
            if value is None:
                cleaned[key] = value
                continue
            
            # Clean string values
            if isinstance(value, str):
                # Remove extra whitespace
                value = re.sub(r'\s+', ' ', value.strip())
                
                # Remove special characters from beginning/end
                value = value.strip('.,;:')
                
                # Convert empty strings to None
                if not value:
                    value = None
            
            # Clean lists
            elif isinstance(value, list):
                value = [self._clean_string(item) if isinstance(item, str) else item 
                        for item in value]
                value = [item for item in value if item]  # Remove empty items
            
            cleaned[key] = value
        
        return cleaned
    
    def _clean_string(self, text: str) -> str:
        """
        Clean individual string.
        
        Args:
            text: String to clean
            
        Returns:
            Cleaned string
        """
        if not text:
            return text
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters from beginning/end
        text = text.strip('.,;:')
        
        return text if text else None
