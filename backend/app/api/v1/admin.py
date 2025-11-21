"""
Admin API router for dashboard, ETL management, and activity validation.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin import get_current_admin
from app.core.dependencies import get_db
from app.models.user import Usuario
from app.services.admin_service import AdminService
from app.schemas.admin import (
    DashboardMetrics,
    ETLStatusResponse,
    ETLExecutionListItem,
    ETLExecutionDetail,
    ETLTriggerRequest,
    ETLTriggerResponse,
    PendingActivity,
    ActivityApprovalRequest,
    ActivityApprovalResponse,
)
import json

router = APIRouter(prefix="/admin", tags=["admin"])


# ========== Dashboard Endpoints ==========

@router.get(
    "/dashboard",
    response_model=DashboardMetrics,
    summary="Get dashboard metrics",
    description="Get comprehensive metrics for admin dashboard (cached for 5 min)"
)
async def get_dashboard_metrics(
    current_admin: Usuario = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard metrics including users, activities, engagement, and ETL stats."""
    admin_service = AdminService(db)
    metrics = await admin_service.get_dashboard_metrics()
    return metrics


# ========== ETL Management Endpoints ==========

@router.get(
    "/etl/status",
    response_model=ETLStatusResponse,
    summary="Get current ETL status",
    description="Get status of currently running or last ETL execution"
)
async def get_etl_status(
    current_admin: Usuario = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get current ETL status or last execution."""
    admin_service = AdminService(db)
    status_data = await admin_service.get_etl_status()
    
    if not status_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No ETL executions found"
        )
    
    return status_data


@router.get(
    "/etl/executions",
    response_model=List[ETLExecutionListItem],
    summary="Get ETL execution history",
    description="Get paginated list of ETL executions"
)
async def get_etl_executions(
    limit: int = 20,
    offset: int = 0,
    current_admin: Usuario = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get ETL execution history with pagination."""
    admin_service = AdminService(db)
    executions = await admin_service.get_etl_executions(limit=limit, offset=offset)
    return executions


@router.get(
    "/etl/executions/{execution_id}",
    response_model=ETLExecutionDetail,
    summary="Get ETL execution details",
    description="Get detailed information for a specific ETL execution"
)
async def get_etl_execution_detail(
    execution_id: int,
    current_admin: Usuario = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information for a specific ETL execution."""
    admin_service = AdminService(db)
    execution = await admin_service.get_etl_execution_detail(execution_id)
    
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ETL execution {execution_id} not found"
        )
    
    return execution


@router.post(
    "/etl/run",
    response_model=ETLTriggerResponse,
    summary="Trigger ETL execution",
    description="Manually trigger an ETL job"
)
async def trigger_etl(
    request: ETLTriggerRequest,
    current_admin: Usuario = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger a manual ETL execution.
    
    This creates an ETL execution record and returns its ID.
    The actual ETL job should be run separately (e.g., via Docker service).
    """
    admin_service = AdminService(db)
    
    # Create execution record
    config_json = json.dumps(request.config) if request.config else None
    execution = await admin_service.create_etl_execution(
        source=request.source,
        triggered_by=f"admin:{current_admin.id}",
        config=config_json
    )
    
    # TODO: Trigger actual ETL Docker service here
    # For now, just return the execution ID
    # In production, this would call: docker compose run etl python src/main.py --execution-id {execution.id}
    
    return {
        "execution_id": execution.id,
        "status": execution.status,
        "message": f"ETL execution {execution.id} created. Job will run asynchronously."
    }


# ========== Activity Validation Endpoints ==========

@router.get(
    "/actividades/pendientes",
    response_model=List[PendingActivity],
    summary="Get pending activities",
    description="Get activities pending validation"
)
async def get_pending_activities(
    limit: int = 50,
    offset: int = 0,
    current_admin: Usuario = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get activities pending validation with pagination."""
    admin_service = AdminService(db)
    activities = await admin_service.get_pending_activities(limit=limit, offset=offset)
    return activities


@router.post(
    "/actividades/aprobar",
    response_model=ActivityApprovalResponse,
    summary="Approve activity",
    description="Approve a pending activity"
)
async def approve_activity(
    request: ActivityApprovalRequest,
    current_admin: Usuario = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Approve a pending activity."""
    admin_service = AdminService(db)
    success = await admin_service.approve_activity(request.activity_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity {request.activity_id} not found"
        )
    
    return {
        "success": True,
        "message": f"Activity {request.activity_id} approved successfully"
    }


@router.post(
    "/actividades/rechazar",
    response_model=ActivityApprovalResponse,
    summary="Reject activity",
    description="Reject a pending activity"
)
async def reject_activity(
    request: ActivityApprovalRequest,
    current_admin: Usuario = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Reject a pending activity."""
    admin_service = AdminService(db)
    success = await admin_service.reject_activity(request.activity_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity {request.activity_id} not found"
        )
    
    return {
        "success": True,
        "message": f"Activity {request.activity_id} rejected successfully"
    }
