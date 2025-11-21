"""
Admin API router for dashboard, ETL management, and activity validation.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin import get_current_admin
from app.core.dependencies import get_db
from app.models.user import Usuario
from app.models.etl_execution import ETLStatus
from app.services.admin_service import AdminService
from app.services.etl_service import ETLService
from app.db.session import async_session_maker
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
import asyncio

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


@router.post(
    "/etl/upload-csv",
    response_model=ETLTriggerResponse,
    summary="Upload CSV and trigger ETL",
    description="Upload a CSV file and automatically trigger ETL processing"
)
async def upload_csv_and_run_etl(
    file: UploadFile,
    current_admin: Usuario = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a CSV file and trigger ETL processing.
    
    Args:
        file: CSV file to upload
        current_admin: Current admin user
        db: Database session
        
    Returns:
        ETL execution details
    """
    import os
    import shutil
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Validate file extension  
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )
    
    # Validate file size (max 10MB)
    try:
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds 10MB limit"
            )
    except Exception as e:
        logger.error(f"Error checking file size: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file: {str(e)}"
        )
    
    admin_service = AdminService(db)
    
    try:
        # Save file in etl/data directory (mounted volume shared with ETL container)
        upload_dir = "/etl/data"
        
        # Ensure directory exists
        os.makedirs(upload_dir, exist_ok=True)
        
        # Create unique filename with timestamp
        from datetime import datetime
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"upload_{timestamp}_{file.filename}"
        file_path = os.path.join(upload_dir, safe_filename)
        
        logger.info(f"Saving uploaded file to: {file_path}")
        
        # Write uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File saved successfully: {safe_filename}")
        
        # Create execution record with file path in config
        execution = await admin_service.create_etl_execution(
            source="csv_upload",
            triggered_by=f"admin:{current_admin.id}",
            config=json.dumps({
                "original_filename": file.filename,
                "saved_filename": safe_filename,
                "file_path": f"/etl/data/{safe_filename}"
            })
        )
        
        logger.info(f"ETL execution record created: {execution.id}")
        
        # Run ETL pipeline asynchronously in background with its own database session
        async def run_etl_background():
            """Run ETL in background task with its own database session."""
            # Create a new database session for the background task
            async with async_session_maker() as background_db:
                try:
                    etl_service = ETLService(background_db)
                    await etl_service.run_csv_etl(execution.id, file_path)
                except Exception as e:
                    logger.error(f"ETL background task failed: {e}", exc_info=True)
                    # Try to update execution status to failed
                    try:
                        async with async_session_maker() as error_db:
                            admin_service = AdminService(error_db)
                            await admin_service.update_etl_status(
                                execution.id,
                                ETLStatus.FAILED,
                                str(e)[:500]
                            )
                    except Exception as update_error:
                        logger.error(f"Failed to update ETL execution status: {update_error}")
        
        # Start ETL in background (fire and forget)
        asyncio.create_task(run_etl_background())
        logger.info(f"ETL pipeline started in background for execution {execution.id}")
        
        return {
            "execution_id": execution.id,
            "status": execution.status,
            "message": f"CSV '{file.filename}' uploaded successfully. ETL processing started automatically."
        }
        
    except Exception as e:
        logger.error(f"Error in upload_csv_and_run_etl: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )



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
