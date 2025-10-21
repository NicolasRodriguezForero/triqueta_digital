"""
SQLAlchemy declarative base and base model.
"""
from datetime import datetime
from typing import Any
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base, declared_attr


class CustomBase:
    """
    Base class with common columns for all models.
    """
    
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically from class name."""
        return cls.__name__.lower()
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


# Create declarative base
Base = declarative_base(cls=CustomBase)
