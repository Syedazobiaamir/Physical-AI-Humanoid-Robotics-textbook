"""
Base model classes with common fields
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from datetime import datetime
import uuid


def generate_uuid():
    """Generate a UUID string"""
    return str(uuid.uuid4())


class BaseModel:
    """Base model with common fields"""
    id = Column(String, primary_key=True, default=generate_uuid)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
