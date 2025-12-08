"""
Translation API endpoints for Urdu content translation
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional

from ..database.base import get_db
from ..auth.dependencies import get_current_user_optional
from ..services.translation_service import TranslationService
from ..models.chapter import Chapter
from ..utils.logger import logger

router = APIRouter()


# Pydantic Schemas
class TranslateUrduRequest(BaseModel):
    """Urdu translation request"""
    content: str = Field(..., description="Content to translate", min_length=1)
    content_type: str = Field(default="text", description="Content type: 'chapter', 'section', or 'text'")
    preserve_formatting: bool = Field(default=True, description="Preserve code blocks and markdown formatting")


class TranslateUrduResponse(BaseModel):
    """Urdu translation response"""
    urdu_content: str
    cache_hit: bool


class CachedTranslationResponse(BaseModel):
    """Cached chapter translation response"""
    urdu_content: str
    last_updated: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    message: Optional[str] = None


# Rate limiting configuration (in production, use Redis or similar)
_request_counts: dict = {}


@router.post("/urdu", response_model=TranslateUrduResponse)
async def translate_to_urdu(
    request: TranslateUrduRequest,
    current_user: Optional[dict] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    Translate content to Urdu

    - **content**: Text content to translate
    - **content_type**: Type of content ('chapter', 'section', 'text')
    - **preserve_formatting**: Whether to preserve code blocks and markdown

    Supports both authenticated and unauthenticated requests.
    Authenticated users have higher rate limits.
    """
    # Validate content type
    if request.content_type not in ("chapter", "section", "text"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_content", "message": "content_type must be 'chapter', 'section', or 'text'"}
        )

    # Check content length limits
    max_length = 50000  # 50KB limit
    if len(request.content) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_content", "message": f"Content exceeds maximum length of {max_length} characters"}
        )

    try:
        service = TranslationService(db)

        # For chapter-type content, we don't have chapter_id so no caching
        # For specific chapter translations, use the GET endpoint
        urdu_content, cache_hit = await service.translate_to_urdu(
            content=request.content,
            chapter_id=None,  # No caching for ad-hoc translations
            preserve_formatting=request.preserve_formatting
        )

        logger.info(f"Translated content of type {request.content_type}, cache_hit={cache_hit}")
        return TranslateUrduResponse(
            urdu_content=urdu_content,
            cache_hit=cache_hit
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "translation_failed", "message": "Failed to translate content"}
        )


@router.get("/urdu/{chapter_id}", response_model=CachedTranslationResponse)
async def get_chapter_urdu_translation(
    chapter_id: str,
    current_user: Optional[dict] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    Get cached Urdu translation for a chapter

    - **chapter_id**: Chapter identifier

    Returns the cached translation if available, otherwise generates a new one.
    """
    try:
        # Verify chapter exists
        result = await db.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        chapter = result.scalar_one_or_none()

        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "chapter_not_found", "message": f"Chapter not found: {chapter_id}"}
            )

        service = TranslationService(db)

        # Try to get cached translation first
        cached_translation = await service.get_chapter_translation(chapter_id)

        if cached_translation:
            return CachedTranslationResponse(
                urdu_content=cached_translation["urdu_content"],
                last_updated=cached_translation["last_updated"]
            )

        # If no cache, translate the chapter content
        urdu_content, _ = await service.translate_to_urdu(
            content=chapter.content,
            chapter_id=chapter_id,
            preserve_formatting=True
        )

        return CachedTranslationResponse(
            urdu_content=urdu_content,
            last_updated=None  # Freshly translated
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chapter translation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "translation_failed", "message": "Failed to get chapter translation"}
        )


@router.post("/urdu/{chapter_id}/refresh", response_model=CachedTranslationResponse)
async def refresh_chapter_translation(
    chapter_id: str,
    current_user: dict = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """
    Force refresh the Urdu translation for a chapter

    - **chapter_id**: Chapter identifier

    This endpoint forces a new translation even if a cached version exists.
    Useful when chapter content has been updated.
    """
    try:
        # Verify chapter exists
        result = await db.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        chapter = result.scalar_one_or_none()

        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "chapter_not_found", "message": f"Chapter not found: {chapter_id}"}
            )

        service = TranslationService(db)

        # Force new translation by not checking cache
        urdu_content, _ = await service.translate_to_urdu(
            content=chapter.content,
            chapter_id=chapter_id,
            preserve_formatting=True
        )

        logger.info(f"Refreshed translation for chapter {chapter_id}")
        return CachedTranslationResponse(
            urdu_content=urdu_content,
            last_updated=None  # Freshly translated
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refreshing chapter translation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "translation_failed", "message": "Failed to refresh chapter translation"}
        )
