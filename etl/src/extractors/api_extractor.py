"""
Generic API extractor.
"""
from typing import List, Dict, Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from src.extractors.base_extractor import BaseExtractor


class APIExtractor(BaseExtractor):
    """Generic API extractor for REST APIs."""
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def extract(self, config: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Extract data from generic API.
        
        Args:
            config: Must contain 'url' and optionally 'headers', 'params', 'json_path'
            
        Returns:
            List of records
        """
        if not config or 'url' not in config:
            raise ValueError("API extractor requires 'url' in config")
        
        url = config['url']
        headers = config.get('headers', {})
        params = config.get('params', {})
        json_path = config.get('json_path', None)  # Path to data in JSON response
        
        self.logger.info(f"Extracting from API: {url}")
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # If json_path is specified, navigate to that path in the response
        if json_path:
            for key in json_path.split('.'):
                data = data[key]
        
        # Ensure data is a list
        if not isinstance(data, list):
            data = [data]
        
        self.log_extraction_stats(data)
        return data
