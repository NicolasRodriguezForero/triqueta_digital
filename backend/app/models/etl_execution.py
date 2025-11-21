"""
ETL Execution model for tracking ETL job executions.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum
import enum

from app.db.base import Base


class ETLStatus(str, enum.Enum):
    """ETL execution status enum."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ETLExecution(Base):
    """
    ETL Execution model for tracking ETL jobs.
    
    Attributes:
        id: Primary key
        status: Execution status (pending, running, success, failed, cancelled)
        started_at: Job start timestamp
        finished_at: Job completion timestamp
        source: Data source (e.g., 'idrd', 'csv', 'api')
        records_extracted: Number of records extracted
        records_transformed: Number of records successfully transformed
        records_loaded: Number of records loaded to DB
        records_failed: Number of records that failed
        error_message: Error message if failed
        log_file_path: Optional path to detailed log file
        triggered_by: User ID or 'system' if automatic
        config: JSON string with execution configuration
    """
    __tablename__ = "etl_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(SQLEnum(ETLStatus), default=ETLStatus.PENDING, nullable=False, index=True)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    
    # Source and metrics
    source = Column(String(100), nullable=False, index=True)
    records_extracted = Column(Integer, default=0, nullable=False)
    records_transformed = Column(Integer, default=0, nullable=False)
    records_loaded = Column(Integer, default=0, nullable=False)
    records_failed = Column(Integer, default=0, nullable=False)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    log_file_path = Column(String(500), nullable=True)
    
    # Metadata
    triggered_by = Column(String(100), nullable=False)  # user_id or 'system'
    config = Column(Text, nullable=True)  # JSON config
