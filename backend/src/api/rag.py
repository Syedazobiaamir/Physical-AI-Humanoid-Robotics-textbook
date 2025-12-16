"""
RAG API endpoints for question answering
"""
import time
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from ..services.rag_service import rag_service
from ..services.skills.context_selection import context_selection
from ..utils.logger import logger

router = APIRouter()


# Request/Response schemas
class RAGQueryRequest(BaseModel):
    """Request schema for RAG query"""
    query: str = Field(..., min_length=1, max_length=2000, description="User's question")
    context_mode: str = Field(
        default="general",
        description="Context mode: 'selection' for selected text, 'general' for broad search"
    )
    selected_text: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Text selected by user (required if context_mode is 'selection')"
    )
    chapter_id: Optional[str] = Field(
        default=None,
        description="Chapter ID to filter search results"
    )
    user_level: Optional[str] = Field(
        default="intermediate",
        description="User's knowledge level: beginner, intermediate, advanced"
    )


class RAGQueryResponse(BaseModel):
    """Response schema for RAG query"""
    answer: str
    sources: List[str]
    latency: float
    related_concepts: Optional[List[str]] = None


class RAGHealthResponse(BaseModel):
    """Response schema for RAG health check"""
    status: str
    models: List[str]
    vector_count: Optional[int] = None
    components: dict


@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(request: RAGQueryRequest):
    """
    Query the RAG system for answers

    - **query**: The user's question (required)
    - **context_mode**: 'selection' for selected text context, 'general' for broad search
    - **selected_text**: Text selected by user (required if context_mode is 'selection')
    - **chapter_id**: Optional chapter ID to filter results
    - **user_level**: User's knowledge level for personalized responses

    Returns an AI-generated answer based on textbook content.
    """
    start_time = time.time()

    try:
        # Validate request
        if request.context_mode == "selection" and not request.selected_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="selected_text is required when context_mode is 'selection'"
            )

        # Use context_selection skill for selected text queries
        if request.context_mode == "selection" and request.selected_text:
            result = await context_selection(
                question=request.query,
                selected_text=request.selected_text,
                chapter_id=request.chapter_id,
                expand_context=True,
                user_level=request.user_level or "intermediate"
            )

            latency = time.time() - start_time

            if not result.get("success"):
                # Fallback to general RAG if context_selection fails
                logger.warning("context_selection skill failed, falling back to RAG")
                result = await rag_service.query(
                    query=request.query,
                    context_mode=request.context_mode,
                    selected_text=request.selected_text,
                    chapter_id=request.chapter_id
                )
                return RAGQueryResponse(
                    answer=result["answer"],
                    sources=result["sources"],
                    latency=result["latency"],
                    related_concepts=None
                )

            return RAGQueryResponse(
                answer=result["answer"],
                sources=result.get("sources", []),
                latency=round(latency, 3),
                related_concepts=result.get("related_concepts", [])
            )

        # Use general RAG for broad queries
        result = await rag_service.query(
            query=request.query,
            context_mode=request.context_mode,
            selected_text=request.selected_text,
            chapter_id=request.chapter_id
        )

        # Check for errors
        if result.get("model") == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("answer", "An error occurred")
            )

        return RAGQueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            latency=result["latency"],
            related_concepts=None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in RAG query endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process query"
        )


@router.get("/health", response_model=RAGHealthResponse)
async def get_rag_health():
    """
    Check RAG system health

    Returns status of all RAG components including:
    - Vector store connectivity
    - OpenAI API availability
    - Anthropic API availability (fallback)
    """
    try:
        health = await rag_service.get_health()

        return RAGHealthResponse(
            status=health["status"],
            models=health.get("providers", []),
            vector_count=health.get("vector_count"),
            components=health["components"]
        )

    except Exception as e:
        logger.error(f"Error in RAG health endpoint: {str(e)}")
        return RAGHealthResponse(
            status="error",
            models=[],
            vector_count=None,
            components={"error": str(e)}
        )
