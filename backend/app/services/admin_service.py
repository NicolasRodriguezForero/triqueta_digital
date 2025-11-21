"""
Admin service for dashboard metrics and management operations.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Usuario
from app.models.activity import Actividad
from app.models.favorite import Favorito
from app.models.etl_execution import ETLExecution, ETLStatus
from app.utils.redis_client import get_redis


class AdminService:
    """Service for admin operations and dashboard metrics."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ========== Dashboard Metrics ==========
    
    async def get_dashboard_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard metrics.
        
        Returns:
            Dict with users, activities, and engagement metrics
        """
        # Try to get from cache
        redis = get_redis()
        cache_key = "admin:dashboard:metrics"
        if redis:
            cached = await redis.get(cache_key)
            if cached:
                import json
                return json.loads(cached)
        
        # Calculate metrics
        metrics = {
            "users": await self._get_user_metrics(),
            "activities": await self._get_activity_metrics(),
            "engagement": await self._get_engagement_metrics(),
            "etl": await self._get_etl_metrics()
        }
        
        # Cache for 5 minutes
        if redis:
            import json
            await redis.setex(cache_key, 300, json.dumps(metrics))
        
        return metrics
    
    async def _get_user_metrics(self) -> Dict[str, int]:
        """Get user-related metrics."""
        # Total users
        total_users_query = select(func.count(Usuario.id))
        total_users_result = await self.db.execute(total_users_query)
        total_users = total_users_result.scalar_one()
        
        # Active users (with profiles)
        active_users_query = select(func.count(Usuario.id)).where(
            Usuario.perfil != None,
            Usuario.is_active == True
        )
        active_users_result = await self.db.execute(active_users_query)
        active_users = active_users_result.scalar_one()
        
        # Admin users
        admin_users_query = select(func.count(Usuario.id)).where(Usuario.is_admin == True)
        admin_users_result = await self.db.execute(admin_users_query)
        admin_users = admin_users_result.scalar_one()
        
        return {
            "total": total_users,
            "active": active_users,
            "admins": admin_users
        }
    
    async def _get_activity_metrics(self) -> Dict[str, Any]:
        """Get activity-related metrics."""
        # Total activities
        total_query = select(func.count(Actividad.id))
        total_result = await self.db.execute(total_query)
        total = total_result.scalar_one()
        
        # By state
        by_state_query = select(
            Actividad.estado,
            func.count(Actividad.id).label('count')
        ).group_by(Actividad.estado)
        by_state_result = await self.db.execute(by_state_query)
        by_state = {row.estado: row.count for row in by_state_result}
        
        # By locality
        by_locality_query = select(
            Actividad.localidad,
            func.count(Actividad.id).label('count')
        ).group_by(Actividad.localidad)
        by_locality_result = await self.db.execute(by_locality_query)
        by_locality = {row.localidad: row.count for row in by_locality_result}
        
        # By type
        by_type_query = select(
            Actividad.tipo,
            func.count(Actividad.id).label('count')
        ).group_by(Actividad.tipo)
        by_type_result = await self.db.execute(by_type_query)
        by_type = {row.tipo: row.count for row in by_type_result}
        
        return {
            "total": total,
            "by_state": by_state,
            "by_locality": by_locality,
            "by_type": by_type
        }
    
    async def _get_engagement_metrics(self) -> Dict[str, Any]:
        """Get engagement metrics."""
        # Total favorites
        total_favs_query = select(func.count(Favorito.id))
        total_favs_result = await self.db.execute(total_favs_query)
        total_favorites = total_favs_result.scalar_one()
        
        # Top 10 popular activities
        top_activities_query = select(
            Actividad.id,
            Actividad.titulo,
            Actividad.popularidad_favoritos,
            Actividad.popularidad_vistas
        ).order_by(
            desc(Actividad.popularidad_favoritos),
            desc(Actividad.popularidad_vistas)
        ).limit(10)
        top_activities_result = await self.db.execute(top_activities_query)
        top_activities = [
            {
                "id": str(row.id),
                "titulo": row.titulo,
                "total_favoritos": row.popularidad_favoritos,
                "total_vistas": float(row.popularidad_vistas)
            }
            for row in top_activities_result
        ]
        
        return {
            "total_favorites": total_favorites,
            "top_activities": top_activities
        }
    
    async def _get_etl_metrics(self) -> Dict[str, Any]:
        """Get ETL execution metrics."""
        # Last 5 executions
        last_executions_query = select(ETLExecution).order_by(
            desc(ETLExecution.started_at)
        ).limit(5)
        last_executions_result = await self.db.execute(last_executions_query)
        last_executions = [
            {
                "id": row.id,
                "status": row.status,
                "source": row.source,
                "started_at": row.started_at.isoformat() if row.started_at else None,
                "finished_at": row.finished_at.isoformat() if row.finished_at else None,
                "records_loaded": row.records_loaded,
                "records_failed": row.records_failed
            }
            for row in last_executions_result.scalars()
        ]
        
        # Success rate
        total_executions_query = select(func.count(ETLExecution.id))
        total_executions_result = await self.db.execute(total_executions_query)
        total_executions = total_executions_result.scalar_one()
        
        success_executions_query = select(func.count(ETLExecution.id)).where(
            ETLExecution.status == ETLStatus.SUCCESS
        )
        success_executions_result = await self.db.execute(success_executions_query)
        success_executions = success_executions_result.scalar_one()
        
        success_rate = (success_executions / total_executions * 100) if total_executions > 0 else 0
        
        return {
            "total_executions": total_executions,
            "success_executions": success_executions,
            "success_rate": round(success_rate, 2),
            "last_executions": last_executions
        }
    
    # ========== ETL Management ==========
    
    async def get_etl_status(self) -> Optional[Dict[str, Any]]:
        """
        Get current ETL status (running or last execution).
        
        Returns:
            Dict with current/last ETL execution info or None
        """
        # Check for running execution
        running_query = select(ETLExecution).where(
            ETLExecution.status == ETLStatus.RUNNING
        ).order_by(desc(ETLExecution.started_at)).limit(1)
        running_result = await self.db.execute(running_query)
        running = running_result.scalar_one_or_none()
        
        if running:
            return {
                "id": running.id,
                "status": running.status,
                "source": running.source,
                "started_at": running.started_at.isoformat(),
                "records_extracted": running.records_extracted,
                "records_transformed": running.records_transformed,
                "records_loaded": running.records_loaded,
                "records_failed": running.records_failed
            }
        
        # Get last execution
        last_query = select(ETLExecution).order_by(
            desc(ETLExecution.started_at)
        ).limit(1)
        last_result = await self.db.execute(last_query)
        last = last_result.scalar_one_or_none()
        
        if last:
            return {
                "id": last.id,
                "status": last.status,
                "source": last.source,
                "started_at": last.started_at.isoformat(),
                "finished_at": last.finished_at.isoformat() if last.finished_at else None,
                "records_extracted": last.records_extracted,
                "records_transformed": last.records_transformed,
                "records_loaded": last.records_loaded,
                "records_failed": last.records_failed,
                "error_message": last.error_message
            }
        
        return None
    
    async def get_etl_executions(
        self,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get ETL execution history.
        
        Args:
            limit: Number of records to return
            offset: Number of records to skip
            
        Returns:
            List of ETL execution records
        """
        query = select(ETLExecution).order_by(
            desc(ETLExecution.started_at)
        ).limit(limit).offset(offset)
        result = await self.db.execute(query)
        
        return [
            {
                "id": row.id,
                "status": row.status,
                "source": row.source,
                "started_at": row.started_at.isoformat(),
                "finished_at": row.finished_at.isoformat() if row.finished_at else None,
                "records_extracted": row.records_extracted,
                "records_transformed": row.records_transformed,
                "records_loaded": row.records_loaded,
                "records_failed": row.records_failed,
                "error_message": row.error_message,
                "triggered_by": row.triggered_by
            }
            for row in result.scalars()
        ]
    
    async def get_etl_execution_detail(self, execution_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed info for a specific ETL execution.
        
        Args:
            execution_id: ETL execution ID
            
        Returns:
            Dict with execution details or None if not found
        """
        query = select(ETLExecution).where(ETLExecution.id == execution_id)
        result = await self.db.execute(query)
        execution = result.scalar_one_or_none()
        
        if not execution:
            return None
        
        return {
            "id": execution.id,
            "status": execution.status,
            "source": execution.source,
            "started_at": execution.started_at.isoformat(),
            "finished_at": execution.finished_at.isoformat() if execution.finished_at else None,
            "records_extracted": execution.records_extracted,
            "records_transformed": execution.records_transformed,
            "records_loaded": execution.records_loaded,
            "records_failed": execution.records_failed,
            "error_message": execution.error_message,
            "log_file_path": execution.log_file_path,
            "triggered_by": execution.triggered_by,
            "config": execution.config
        }
    
    async def create_etl_execution(
        self,
        source: str,
        triggered_by: str,
        config: Optional[str] = None
    ) -> ETLExecution:
        """
        Create a new ETL execution record.
        
        Args:
            source: Data source name
            triggered_by: User ID or 'system'
            config: Optional JSON config
            
        Returns:
            Created ETLExecution instance
        """
        execution = ETLExecution(
            source=source,
            triggered_by=triggered_by,
            config=config,
            status=ETLStatus.PENDING
        )
        self.db.add(execution)
        await self.db.commit()
        await self.db.refresh(execution)
        return execution
    
    async def update_etl_status(
        self,
        execution_id: int,
        status: ETLStatus,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Update ETL execution status.
        
        Args:
            execution_id: ETL execution ID
            status: New status
            error_message: Optional error message
            
        Returns:
            True if updated, False if not found
        """
        query = select(ETLExecution).where(ETLExecution.id == execution_id)
        result = await self.db.execute(query)
        execution = result.scalar_one_or_none()
        
        if not execution:
            return False
        
        execution.status = status
        if error_message:
            execution.error_message = error_message
        if status in [ETLStatus.SUCCESS, ETLStatus.FAILED]:
            execution.finished_at = datetime.utcnow()
        
        await self.db.commit()
        return True

    # ========== Activity Validation ==========
    
    async def get_pending_activities(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get activities pending validation.
        
        Args:
            limit: Number of records to return
            offset: Number of records to skip
            
        Returns:
            List of pending activities
        """
        query = select(Actividad).where(
            Actividad.estado == "pendiente"
        ).order_by(desc(Actividad.created_at)).limit(limit).offset(offset)
        result = await self.db.execute(query)
        
        return [
            {
                "id": str(row.id),
                "titulo": row.titulo,
                "descripcion": row.descripcion,
                "tipo": row.tipo,
                "localidad": row.localidad,
                "ubicacion_direccion": row.ubicacion_direccion,
                "fecha_inicio": row.fecha_inicio.isoformat() if row.fecha_inicio else None,
                "fecha_fin": row.fecha_fin.isoformat() if row.fecha_fin else None,
                "precio": float(row.precio),
                "es_gratis": row.es_gratis,
                "created_at": row.created_at.isoformat(),
                "fuente": row.fuente
            }
            for row in result.scalars()
        ]
    
    async def approve_activity(self, activity_id: int) -> bool:
        """
        Approve a pending activity.
        
        Args:
            activity_id: Activity ID
            
        Returns:
            True if approved, False if not found
        """
        query = select(Actividad).where(Actividad.id == activity_id)
        result = await self.db.execute(query)
        activity = result.scalar_one_or_none()
        
        if not activity:
            return False
        
        activity.estado = "activa"
        await self.db.commit()
        return True
    
    async def reject_activity(self, activity_id: int) -> bool:
        """
        Reject a pending activity.
        
        Args:
            activity_id: Activity ID
            
        Returns:
            True if rejected, False if not found
        """
        query = select(Actividad).where(Actividad.id == activity_id)
        result = await self.db.execute(query)
        activity = result.scalar_one_or_none()
        
        if not activity:
            return False
        
        activity.estado = "cancelada"
        await self.db.commit()
        return True
