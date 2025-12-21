"""
ProgressTracking model for tracking user progress through chapters
"""
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database.base import Base
from .base import BaseModel


class ProgressTracking(Base, BaseModel):
    """
    ProgressTracking entity for tracking user progress through chapters

    Attributes:
        id: Unique progress record identifier
        user_id: Reference to user
        chapter_id: Reference to chapter
        status: Progress status (not_started, in_progress, completed, reviewed)
        quiz_score: Score on chapter quiz (0-100)
        time_spent_seconds: Total time spent on chapter
        completed_at: Completion timestamp
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "progress_tracking"

    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(String(255), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="not_started")
    quiz_score = Column(Integer, nullable=True)
    time_spent_seconds = Column(Integer, nullable=True, default=0)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship
    user = relationship("User", back_populates="progress_records")

    def __repr__(self):
        return f"<ProgressTracking(id={self.id}, user_id={self.user_id}, chapter_id={self.chapter_id}, status={self.status})>"

    def to_dict(self):
        """Convert progress record to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "chapter_id": self.chapter_id,
            "status": self.status,
            "quiz_score": self.quiz_score,
            "time_spent_seconds": self.time_spent_seconds,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
