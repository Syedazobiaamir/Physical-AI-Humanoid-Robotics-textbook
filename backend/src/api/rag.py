"""
RAG API endpoints for question answering
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from ..services.rag_service import rag_service
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


class RAGQueryResponse(BaseModel):
    """Response schema for RAG query"""
    answer: str
    sources: List[str]
    latency: float


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

    Returns an AI-generated answer based on textbook content.
    """
    try:
        # Validate request
        if request.context_mode == "selection" and not request.selected_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="selected_text is required when context_mode is 'selection'"
            )

        # Process query
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
            latency=result["latency"]
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
            models=health["models"],
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
