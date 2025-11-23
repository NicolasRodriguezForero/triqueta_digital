"""
IDRD API extractor.
"""
from typing import List, Dict, Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from src.extractors.base_extractor import BaseExtractor


class IDRDExtractor(BaseExtractor):
    """Extract data from IDRD API."""
    
    # IDRD might have different endpoints - this is a placeholder
    # You'll need to adjust this based on actual IDRD API documentation
    BASE_URL = "https://datosabiertos.bogota.gov.co/api/"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def extract(self, config: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Extract data from IDRD API.
        
        Args:
            config: Optional configuration (endpoint, params, etc.)
            
        Returns:
            List of activities from IDRD
        """
        # For MVP, we'll use a mock implementation
        # In production, replace with actual IDRD API calls
        
        self.logger.info("Extracting from IDRD API (MOCK)")
        self.logger.warning("IDRD extractor is using mock data. Configure real API endpoint.")
        
        # Mock data structure based on typical IDRD format
        mock_records = [
            {
                "nombre": "Fútbol Recreativo - Parque El Virrey",
                "descripcion": "Actividad de fútbol recreativo para todas las edades",
                "tipo": "Deporte",
                "localidad": "Chapinero",
                "direccion": "Parque El Virrey, Calle 88 con Carrera 15",
                "fecha_inicio": "2025-12-01",
                "fecha_fin": "2025-12-31",
                "horario": "Lunes a viernes 6:00 AM - 8:00 AM",
                "precio": 0.0,
                "es_gratuita": True,
                "contacto_telefono": "60112345678",
                "contacto_email": "deportes@idrd.gov.co",
                "etiquetas": ["deporte", "fútbol", "recreación"],
                "fuente": "IDRD"
            },
            {
                "nombre": "Yoga en el Parque - Santa Fe",
                "descripcion": "Clases gratuitas de yoga al aire libre",
                "tipo": "Recreación",
                "localidad": "Santa Fe",
                "direccion": "Parque de los Periodistas",
                "fecha_inicio": "2025-12-01",
                "fecha_fin": "2025-12-31",
                "horario": "Sábados y domingos 8:00 AM - 10:00 AM",
                "precio": 0.0,
                "es_gratuita": True,
                "contacto_telefono": "60112345679",
                "contacto_email": "recreacion@idrd.gov.co",
                "etiquetas": ["yoga", "bienestar", "recreación"],
                "fuente": "IDRD"
            }
        ]
        
        self.log_extraction_stats(mock_records)
        return mock_records
    
    def _call_idrd_api(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make API call to IDRD.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            API response as dict
        """
        url = f"{self.BASE_URL}{endpoint}"
        self.logger.debug(f"Calling IDRD API: {url}")
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        return response.json()
