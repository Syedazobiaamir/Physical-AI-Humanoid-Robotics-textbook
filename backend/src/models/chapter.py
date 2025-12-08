"""
Chapter model for textbook content
"""
from sqlalchemy import Column, String, Integer, JSON, Text
from sqlalchemy.dialects.postgresql import ARRAY
from ..database.base import Base
from .base import BaseModel


class Chapter(Base, BaseModel):
    """
    Chapter entity representing a textbook chapter

    Attributes:
        id: Unique chapter identifier
        title: Chapter title
        module: Module identifier (e.g., "Module 1")
        week: Week number (1-13)
        learning_objectives: List of learning objectives
        content: Full chapter content in MDX format
        code_examples: List of code example metadata
        lab_tasks: List of lab task descriptions
        resources: Additional resources and references
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "chapters"

    title = Column(String(255), nullable=False, index=True)
    module = Column(String(50), nullable=False, index=True)
    week = Column(Integer, nullable=False, index=True)
    learning_objectives = Column(ARRAY(Text), nullable=False, default=[])
    content = Column(Text, nullable=False)
    code_examples = Column(JSON, nullable=True, default=[])
    lab_tasks = Column(JSON, nullable=True, default=[])
    resources = Column(JSON, nullable=True, default=[])

    def __repr__(self):
        return f"<Chapter(id={self.id}, title={self.title}, module={self.module}, week={self.week})>"

    def to_dict(self):
        """Convert chapter to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "module": self.module,
            "week": self.week,
            "learning_objectives": self.learning_objectives,
            "content": self.content,
            "code_examples": self.code_examples or [],
            "lab_tasks": self.lab_tasks or [],
            "resources": self.resources or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
