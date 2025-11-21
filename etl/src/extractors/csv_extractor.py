"""
CSV extractor for local CSV files.
"""
import csv
from typing import List, Dict, Any
from pathlib import Path

from src.extractors.base_extractor import BaseExtractor


class CSVExtractor(BaseExtractor):
    """Extract data from CSV files."""
    
    async def extract(self, config: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Extract data from CSV file.
        
        Args:
            config: Should contain 'file_path' key
            
        Returns:
            List of records as dicts
        """
        if not config or 'file_path' not in config:
            raise ValueError("CSV extractor requires 'file_path' in config")
        
        file_path = Path(config['file_path'])
        
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        self.logger.info(f"Extracting from CSV: {file_path}")
        
        records = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))
        
        self.log_extraction_stats(records)
        return records
