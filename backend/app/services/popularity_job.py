"""
Background job for recalculating activity popularity scores.

Implements requirement RF-015 from SRS.
"""
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
import logging

from app.models.activity import Actividad
from app.db.session import async_session_maker

logger = logging.getLogger(__name__)


async def recalculate_popularity_job():
    """
    Background job to recalculate normalized popularity for all activities.
    
    This should run daily to keep popularity scores updated.
    
    Algorithm:
    1. Calculate max score across all activities
    2. Normalize each activity's score to 0-1 range
    
    Score formula: favoritos * 1.0 + vistas * 0.1
    """
    logger.info("Starting popularity recalculation job")
    
    async with async_session_maker() as db:
        try:
            # Get all active activities
            query = select(Actividad).where(Actividad.estado == "activa")
            result = await db.execute(query)
            activities = result.scalars().all()
            
            if not activities:
                logger.info("No activities to process")
                return
            
            # Calculate raw scores
            scores = []
            for activity in activities:
                raw_score = (
                    float(activity.popularidad_favoritos) * 1.0 +
                    float(activity.popularidad_vistas) * 0.1
                )
                scores.append((activity, raw_score))
            
            # Find max score for normalization
            max_score = max(score for _, score in scores) if scores else 1.0
            
            if max_score == 0:
                max_score = 1.0  # Prevent division by zero
            
            # Update normalized popularity
            updated_count = 0
            for activity, raw_score in scores:
                normalized = Decimal(str(raw_score / max_score))
                activity.popularidad_normalizada = normalized
                updated_count += 1
            
            await db.commit()
            
            logger.info(
                f"Popularity recalculation completed. "
                f"Updated {updated_count} activities. Max score: {max_score:.2f}"
            )
            
        except Exception as e:
            logger.error(f"Error in popularity recalculation job: {str(e)}", exc_info=True)
            await db.rollback()
            raise
