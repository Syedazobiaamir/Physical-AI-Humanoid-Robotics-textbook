"""
User model for platform authentication and profiles
"""
from sqlalchemy import Column, String, Enum, JSON
from sqlalchemy.orm import relationship
from ..database.base import Base
from .base import BaseModel
import enum


class UserRole(str, enum.Enum):
    """User role enumeration"""
    STUDENT = "student"
    AUTHOR = "author"
    ADMIN = "admin"


class SkillLevel(str, enum.Enum):
    """Skill level enumeration for personalization"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class User(Base, BaseModel):
    """
    User entity representing platform users

    Attributes:
        id: Unique user identifier (UUID)
        email: User email address (unique)
        name: User's full name
        role: User role (student, author, admin)
        oauth_provider: OAuth provider used for signup (google, github)
        oauth_id: OAuth provider's user ID
        software_background: User's software experience level
        hardware_background: User's hardware experience level
        preferences: JSON field for user preferences
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default=UserRole.STUDENT.value)
    oauth_provider = Column(String(50), nullable=True)
    oauth_id = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    software_background = Column(String(100), nullable=True)
    hardware_background = Column(String(100), nullable=True)
    preferences = Column(JSON, nullable=True, default={})

    # Relationships
    personalization_profiles = relationship(
        "PersonalizationProfile",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    progress_records = relationship(
        "ProgressTracking",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

    def to_dict(self):
        """Convert user to dictionary (excludes sensitive data)"""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "avatar_url": self.avatar_url,
            "software_background": self.software_background,
            "hardware_background": self.hardware_background,
            "preferences": self.preferences or {},
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def to_jwt_payload(self):
        """Convert user to JWT payload"""
        return {
            "sub": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role
        }
