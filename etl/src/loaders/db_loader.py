"""
Database loader for ETL.
"""
from typing import List, Dict, Any
import logging
from datetime import datetime
import asyncio
from sqlalchemy import create_engine, select, or_, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class DatabaseLoader:
    """Load transformed data into PostgreSQL."""
    
    def __init__(self, database_url: str, logger: logging.Logger = None):
        """
        Initialize database loader.
        
        Args:
            database_url: PostgreSQL connection string
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.database_url = database_url
        
        # Create async engine
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def load(self, records: List[Dict[str, Any]]) -> tuple[int, int, List[str]]:
        """
        Load records into database.
        
        Args:
            records: Validated and normalized records
            
        Returns:
            Tuple of (loaded_count, failed_count, error_messages)
        """
        self.logger.info(f"Loading {len(records)} records to database")
        
        loaded = 0
        failed = 0
        errors = []
        
        async with self.async_session() as session:
            for record in records:
                try:
                    # Import here to avoid circular imports
                    from app.models.activity import Actividad, ActividadEstado
                    
                    # Create activity instance
                    activity = Actividad(
                        nombre=record['nombre'],
                        descripcion=record['descripcion'],
                        tipo=record['tipo'],
                        localidad=record.get('localidad'),
                        direccion=record.get('direccion'),
                        fecha_inicio=record.get('fecha_inicio'),
                        fecha_fin=record.get('fecha_fin'),
                        horario=record.get('horario'),
                        precio=record.get('precio', 0.0),
                        es_gratuita=record.get('es_gratuita', True),
                        contacto_telefono=record.get('contacto_telefono'),
                        contacto_email=record.get('contacto_email'),
                        contacto_web=record.get('contacto_web'),
                        etiquetas=record.get('etiquetas', []),
                        fuente=record['fuente'],
                        estado=ActividadEstado.PENDIENTE  # Requires admin approval
                    )
                    
                    session.add(activity)
                    await session.commit()
                    loaded += 1
                    
                except Exception as e:
                    failed += 1
                    error_msg = f"Failed to load record '{record.get('nombre', 'Unknown')}': {str(e)}"
                    self.logger.error(error_msg)
                    errors.append(error_msg)
                    await session.rollback()
                    continue
        
        self.logger.info(f"Loading complete: {loaded} loaded, {failed} failed")
        return loaded, failed, errors
    
    async def close(self):
        """Close database connection."""
        await self.engine.dispose()
