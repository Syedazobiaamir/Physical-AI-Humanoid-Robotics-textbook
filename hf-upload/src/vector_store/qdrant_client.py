"""
Qdrant vector database client for RAG functionality
"""
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
from typing import List, Dict, Optional, Any
import os
from dotenv import load_dotenv
from ..utils.logger import logger

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_textbook")
VECTOR_SIZE = 768  # Gemini text-embedding-004 dimension


class QdrantVectorStore:
    """
    Qdrant vector store for storing and retrieving document embeddings
    """

    def __init__(self, lazy_init: bool = True):
        """Initialize Qdrant client

        Args:
            lazy_init: If True, defer connection until first use
        """
        self._client = None
        self._initialized = False
        self.collection_name = QDRANT_COLLECTION_NAME

        if not lazy_init:
            self._ensure_initialized()

    @property
    def client(self):
        """Lazily initialize and return the Qdrant client"""
        if self._client is None:
            self._ensure_initialized()
        return self._client

    def _ensure_initialized(self):
        """Initialize connection to Qdrant"""
        if self._initialized:
            return

        try:
            self._client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY if QDRANT_API_KEY else None
            )
            self._ensure_collection()
            self._initialized = True
        except Exception as e:
            logger.warning(f"Qdrant not available: {str(e)}. RAG features will be limited.")
            self._client = None
            self._initialized = True  # Mark as initialized to avoid repeated attempts

    def is_available(self) -> bool:
        """Check if Qdrant is available"""
        if not self._initialized:
            self._ensure_initialized()
        return self._client is not None

    def _ensure_collection(self):
        """Ensure collection exists, create if it doesn't"""
        if self._client is None:
            return

        try:
            collections = self._client.get_collections().collections
            collection_names = [col.name for col in collections]

            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")
                self._client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=VECTOR_SIZE,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Collection created: {self.collection_name}")
            else:
                logger.info(f"Collection already exists: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error ensuring collection: {str(e)}")
            # Don't raise - allow app to start without Qdrant

    def upsert_vectors(
        self,
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> bool:
        """
        Insert or update vectors in the collection

        Args:
            vectors: List of vector embeddings
            payloads: List of metadata dictionaries
            ids: Optional list of point IDs

        Returns:
            True if successful
        """
        if not self.is_available():
            logger.warning("Qdrant not available, skipping upsert")
            return False

        try:
            if ids is None:
                ids = [str(i) for i in range(len(vectors))]

            points = [
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
                for point_id, vector, payload in zip(ids, vectors, payloads)
            ]

            self._client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Upserted {len(points)} vectors to Qdrant")
            return True
        except Exception as e:
            logger.error(f"Error upserting vectors: {str(e)}")
            return False

    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        filter_conditions: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors

        Args:
            query_vector: Query vector embedding
            limit: Number of results to return
            filter_conditions: Optional metadata filters
            score_threshold: Optional minimum similarity score

        Returns:
            List of search results with scores and payloads
        """
        if not self.is_available():
            logger.warning("Qdrant not available, returning empty results")
            return []

        try:
            # Build filter if conditions provided
            search_filter = None
            if filter_conditions:
                conditions = [
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                    for key, value in filter_conditions.items()
                ]
                search_filter = Filter(must=conditions)

            # Perform search using query_points (new API)
            search_result = self._client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                query_filter=search_filter,
                score_threshold=score_threshold
            )

            # Format results
            formatted_results = [
                {
                    "id": point.id,
                    "score": point.score,
                    "payload": point.payload
                }
                for point in search_result.points
            ]

            logger.info(f"Found {len(formatted_results)} results")
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching vectors: {str(e)}")
            return []

    def delete_by_filter(self, filter_conditions: Dict[str, Any]) -> bool:
        """
        Delete vectors matching filter conditions

        Args:
            filter_conditions: Metadata filters for deletion

        Returns:
            True if successful
        """
        if not self.is_available():
            logger.warning("Qdrant not available, skipping delete")
            return False

        try:
            conditions = [
                FieldCondition(
                    key=key,
                    match=MatchValue(value=value)
                )
                for key, value in filter_conditions.items()
            ]
            delete_filter = Filter(must=conditions)

            self._client.delete(
                collection_name=self.collection_name,
                points_selector=delete_filter
            )

            logger.info(f"Deleted vectors matching filter: {filter_conditions}")
            return True
        except Exception as e:
            logger.error(f"Error deleting vectors: {str(e)}")
            return False

    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information"""
        if not self.is_available():
            return {"status": "unavailable", "name": self.collection_name}

        try:
            info = self._client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {"status": "error", "name": self.collection_name}


# Singleton instance
qdrant_store = QdrantVectorStore()
