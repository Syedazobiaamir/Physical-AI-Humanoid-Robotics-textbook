"""
PersonalizationProfile model for user content adaptation preferences
"""
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database.base import Base
from .base import BaseModel


class PersonalizationProfile(Base, BaseModel):
    """
    PersonalizationProfile entity for storing user's skill level preferences per chapter

    Attributes:
        id: Unique profile identifier
        user_id: Reference to user
        chapter_id: Reference to chapter
        skill_level: Preferred skill level (beginner, intermediate, advanced)
        customizations: Additional customization preferences
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "personalization_profiles"

    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(String(255), nullable=False, index=True)
    skill_level = Column(String(50), nullable=False, default="intermediate")
    customizations = Column(JSON, nullable=True, default={})

    # Relationship
    user = relationship("User", back_populates="personalization_profiles")

    def __repr__(self):
        return f"<PersonalizationProfile(id={self.id}, user_id={self.user_id}, chapter_id={self.chapter_id}, skill_level={self.skill_level})>"

    def to_dict(self):
        """Convert profile to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "chapter_id": self.chapter_id,
            "skill_level": self.skill_level,
            "customizations": self.customizations or {},
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
