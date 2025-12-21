"""
VectorChunk model for storing text segments with embeddings
"""
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from ..database.base import Base
from .base import BaseModel


class VectorChunk(Base, BaseModel):
    """
    VectorChunk entity representing a text segment stored in the vector database

    Attributes:
        id: Unique chunk identifier
        doc_id: Document identifier for grouping chunks
        chapter_id: Reference to associated chapter
        heading: Section heading (if applicable)
        chunk_index: Order within document
        content: Text content of the chunk
        embedding_id: Reference to vector in Qdrant
        token_count: Number of tokens in chunk
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "vector_chunks"

    doc_id = Column(String(255), nullable=False, index=True)
    chapter_id = Column(String(255), nullable=False, index=True)
    heading = Column(String(500), nullable=True)
    chunk_index = Column(Integer, nullable=False, default=0)
    content = Column(Text, nullable=False)
    embedding_id = Column(String(255), nullable=True)  # Reference to Qdrant point ID
    token_count = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<VectorChunk(id={self.id}, doc_id={self.doc_id}, chapter_id={self.chapter_id}, index={self.chunk_index})>"

    def to_dict(self):
        """Convert chunk to dictionary"""
        return {
            "id": self.id,
            "doc_id": self.doc_id,
            "chapter_id": self.chapter_id,
            "heading": self.heading,
            "chunk_index": self.chunk_index,
            "content": self.content,
            "embedding_id": self.embedding_id,
            "token_count": self.token_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def to_payload(self):
        """Convert to Qdrant payload format"""
        return {
            "chunk_id": self.id,
            "doc_id": self.doc_id,
            "chapter_id": self.chapter_id,
            "heading": self.heading or "",
            "chunk_index": self.chunk_index,
            "content": self.content
        }
