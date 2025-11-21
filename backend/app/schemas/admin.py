"""
Pydantic schemas for admin operations.
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from app.models.etl_execution import ETLStatus


# ========== Dashboard Schemas ==========

class UserMetrics(BaseModel):
    """User metrics schema."""
    total: int = Field(..., description="Total number of users")
    active: int = Field(..., description="Number of active users")
    admins: int = Field(..., description="Number of admin users")


class ActivityMetrics(BaseModel):
    """Activity metrics schema."""
    total: int = Field(..., description="Total number of activities")
    by_state: Dict[str, int] = Field(..., description="Activities by state")
    by_locality: Dict[str, int] = Field(..., description="Activities by locality")
    by_type: Dict[str, int] = Field(..., description="Activities by type")


class TopActivity(BaseModel):
    """Top activity schema."""
    id: int
    nombre: str
    total_favoritos: int
    total_vistas: int


class EngagementMetrics(BaseModel):
    """Engagement metrics schema."""
    total_favorites: int = Field(..., description="Total number of favorites")
    top_activities: List[TopActivity] = Field(..., description="Top 10 activities")


class ETLExecutionSummary(BaseModel):
    """ETL execution summary schema."""
    id: int
    status: str
    source: str
    started_at: Optional[str]
    finished_at: Optional[str]
    records_loaded: int
    records_failed: int


class ETLMetrics(BaseModel):
    """ETL metrics schema."""
    total_executions: int
    success_executions: int
    success_rate: float
    last_executions: List[ETLExecutionSummary]


class DashboardMetrics(BaseModel):
    """Complete dashboard metrics schema."""
    users: UserMetrics
    activities: ActivityMetrics
    engagement: EngagementMetrics
    etl: ETLMetrics


# ========== ETL Management Schemas ==========

class ETLStatusResponse(BaseModel):
    """ETL status response schema."""
    id: int
    status: str
    source: str
    started_at: str
    finished_at: Optional[str] = None
    records_extracted: int
    records_transformed: int
    records_loaded: int
    records_failed: int
    error_message: Optional[str] = None


class ETLExecutionListItem(BaseModel):
    """ETL execution list item schema."""
    id: int
    status: str
    source: str
    started_at: str
    finished_at: Optional[str]
    records_extracted: int
    records_transformed: int
    records_loaded: int
    records_failed: int
    error_message: Optional[str]
    triggered_by: str


class ETLExecutionDetail(BaseModel):
    """ETL execution detail schema."""
    id: int
    status: str
    source: str
    started_at: str
    finished_at: Optional[str]
    records_extracted: int
    records_transformed: int
    records_loaded: int
    records_failed: int
    error_message: Optional[str]
    log_file_path: Optional[str]
    triggered_by: str
    config: Optional[str]


class ETLTriggerRequest(BaseModel):
    """ETL trigger request schema."""
    source: str = Field(..., description="Source to extract from (idrd, csv, etc.)")
    config: Optional[Dict[str, Any]] = Field(None, description="Optional configuration")


class ETLTriggerResponse(BaseModel):
    """ETL trigger response schema."""
    execution_id: int
    status: str
    message: str


# ========== Activity Validation Schemas ==========

class PendingActivity(BaseModel):
    """Pending activity schema."""
    id: int
    nombre: str
    descripcion: str
    tipo: str
    localidad: str
    direccion: str
    fecha_inicio: Optional[str]
    fecha_fin: Optional[str]
    horario: Optional[str]
    precio: Optional[float]
    es_gratuita: bool
    created_at: str
    fuente: str


class ActivityApprovalRequest(BaseModel):
    """Activity approval request schema."""
    activity_id: int = Field(..., description="Activity ID to approve/reject")


class ActivityApprovalResponse(BaseModel):
    """Activity approval response schema."""
    success: bool
    message: str
