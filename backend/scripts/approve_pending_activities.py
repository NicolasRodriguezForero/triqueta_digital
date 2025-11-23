"""
Script to approve all pending activities (change estado from 'pendiente_validacion' to 'activa').

Usage:
    python scripts/approve_pending_activities.py
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, update
from app.db.session import async_session_maker
from app.models.activity import Actividad


async def approve_all_pending_activities():
    """Approve all activities with estado 'pendiente_validacion'."""
    async with async_session_maker() as db:
        # Get all pending activities
        query = select(Actividad).where(Actividad.estado == "pendiente_validacion")
        result = await db.execute(query)
        pending_activities = result.scalars().all()
        
        if not pending_activities:
            print("No hay actividades pendientes de aprobación.")
            return
        
        print(f"Encontradas {len(pending_activities)} actividades pendientes:")
        for activity in pending_activities:
            print(f"  - {activity.titulo} (ID: {activity.id})")
        
        # Update all to 'activa'
        update_query = update(Actividad).where(
            Actividad.estado == "pendiente_validacion"
        ).values(estado="activa")
        
        result = await db.execute(update_query)
        await db.commit()
        
        print(f"\n✅ {result.rowcount} actividades aprobadas exitosamente.")
        print("Las actividades ahora deberían aparecer en el listado público.")


if __name__ == "__main__":
    asyncio.run(approve_all_pending_activities())

