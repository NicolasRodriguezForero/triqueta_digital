"""
Base extractor class for ETL.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging


class BaseExtractor(ABC):
    """Base class for all extractors."""
    
    def __init__(self, logger: logging.Logger = None):
        """
        Initialize extractor.
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
    
    @abstractmethod
    async def extract(self, config: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Extract data from source.
        
        Args:
            config: Optional configuration dict
            
        Returns:
            List of extracted records as dicts
        """
        pass
    
    def log_extraction_stats(self, records: List[Dict[str, Any]]):
        """
        Log extraction statistics.
        
        Args:
            records: Extracted records
        """
        self.logger.info(f"Extracted {len(records)} records")
        if records:
            self.logger.debug(f"Sample record: {records[0]}")
