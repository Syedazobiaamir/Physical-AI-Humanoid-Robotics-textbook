"""
TranslationCache model for caching Urdu translations
"""
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from ..database.base import Base
from .base import BaseModel


class TranslationCache(Base, BaseModel):
    """
    TranslationCache entity for caching Urdu translations of chapter content

    Attributes:
        id: Unique cache entry identifier
        chapter_id: Reference to chapter
        content_hash: Hash of original content for cache invalidation
        urdu_content: Translated Urdu content
        created_at: Creation timestamp
        expires_at: Expiration timestamp for cache invalidation
    """

    __tablename__ = "translation_cache"

    chapter_id = Column(String(255), nullable=False, index=True)
    content_hash = Column(String(64), nullable=False, index=True)
    urdu_content = Column(Text, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return f"<TranslationCache(id={self.id}, chapter_id={self.chapter_id}, content_hash={self.content_hash[:8]}...)>"

    def to_dict(self):
        """Convert cache entry to dictionary"""
        return {
            "id": self.id,
            "chapter_id": self.chapter_id,
            "content_hash": self.content_hash,
            "urdu_content": self.urdu_content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }

    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc) > self.expires_at
