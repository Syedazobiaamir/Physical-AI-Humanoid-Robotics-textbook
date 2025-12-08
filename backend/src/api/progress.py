"""
Progress tracking API endpoints for user learning progress
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from ..database.base import get_db
from ..auth.dependencies import get_current_user, get_current_admin_user
from ..models.progress_tracking import ProgressTracking
from ..models.user import User
from ..utils.logger import logger

router = APIRouter()


# Pydantic Schemas
class QuizScoreEntry(BaseModel):
    """Quiz score entry"""
    chapter_id: str
    score: int
    completed_at: Optional[str] = None


class ProgressSummaryResponse(BaseModel):
    """User progress summary response"""
    completed_chapters: List[str]
    quiz_scores: List[QuizScoreEntry]
    overall_progress: float


class TrackProgressRequest(BaseModel):
    """Track progress request"""
    chapter_id: str = Field(..., description="Chapter identifier")
    action: str = Field(..., description="Progress action: 'started', 'completed', or 'quiz_completed'")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional metadata")


class TrackProgressResponse(BaseModel):
    """Track progress response"""
    success: bool
    progress_updated: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    message: Optional[str] = None


# Valid progress actions
VALID_ACTIONS = {"started", "completed", "quiz_completed"}

# Status mapping for actions
ACTION_STATUS_MAP = {
    "started": "in_progress",
    "completed": "completed",
    "quiz_completed": "reviewed"
}


@router.get("/user/{user_id}", response_model=ProgressSummaryResponse)
async def get_user_progress(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's progress summary

    - **user_id**: User identifier to get progress for

    Users can only access their own progress unless they are admins.
    """
    requesting_user_id = current_user.get("sub")
    requesting_user_role = current_user.get("role")

    # Check authorization: user can only view own progress unless admin
    if user_id != requesting_user_id and requesting_user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "forbidden", "message": "Cannot access other users' progress"}
        )

    try:
        # Verify user exists
        user_result = await db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "not_found", "message": "User not found"}
            )

        # Get all progress records for user
        result = await db.execute(
            select(ProgressTracking).where(ProgressTracking.user_id == user_id)
        )
        progress_records = result.scalars().all()

        # Calculate completed chapters
        completed_chapters = [
            record.chapter_id
            for record in progress_records
            if record.status in ("completed", "reviewed")
        ]

        # Calculate quiz scores
        quiz_scores = [
            QuizScoreEntry(
                chapter_id=record.chapter_id,
                score=record.quiz_score,
                completed_at=record.completed_at.isoformat() if record.completed_at else None
            )
            for record in progress_records
            if record.quiz_score is not None
        ]

        # Calculate overall progress (percentage of chapters completed)
        # Assuming 13 weeks of content
        total_chapters = 13
        completed_count = len(completed_chapters)
        overall_progress = round((completed_count / total_chapters) * 100, 1) if total_chapters > 0 else 0.0

        return ProgressSummaryResponse(
            completed_chapters=completed_chapters,
            quiz_scores=quiz_scores,
            overall_progress=overall_progress
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user progress: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Failed to retrieve progress"}
        )


@router.post("/track", response_model=TrackProgressResponse)
async def track_progress(
    request: TrackProgressRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update progress for a chapter

    - **chapter_id**: Chapter identifier
    - **action**: Progress action ('started', 'completed', 'quiz_completed')
    - **metadata**: Additional metadata (e.g., quiz score, time spent)
    """
    user_id = current_user.get("sub")

    # Validate action
    if request.action.lower() not in VALID_ACTIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_action", "message": f"Invalid action. Must be one of: {', '.join(VALID_ACTIONS)}"}
        )

    action = request.action.lower()
    new_status = ACTION_STATUS_MAP[action]

    try:
        # Find existing progress record
        result = await db.execute(
            select(ProgressTracking).where(
                ProgressTracking.user_id == user_id,
                ProgressTracking.chapter_id == request.chapter_id
            )
        )
        progress = result.scalar_one_or_none()

        now = datetime.utcnow()

        if progress:
            # Update existing record
            progress.status = new_status
            progress.updated_at = now

            # Handle action-specific updates
            if action == "completed":
                progress.completed_at = now
            elif action == "quiz_completed":
                progress.completed_at = now
                # Extract quiz score from metadata if provided
                if request.metadata and "score" in request.metadata:
                    score = request.metadata["score"]
                    if isinstance(score, (int, float)) and 0 <= score <= 100:
                        progress.quiz_score = int(score)

            # Update time spent if provided
            if request.metadata and "time_spent" in request.metadata:
                time_spent = request.metadata["time_spent"]
                if isinstance(time_spent, int) and time_spent >= 0:
                    progress.time_spent_seconds = (progress.time_spent_seconds or 0) + time_spent
        else:
            # Create new progress record
            progress = ProgressTracking(
                id=str(uuid.uuid4()),
                user_id=user_id,
                chapter_id=request.chapter_id,
                status=new_status
            )

            # Handle action-specific initialization
            if action == "completed":
                progress.completed_at = now
            elif action == "quiz_completed":
                progress.completed_at = now
                if request.metadata and "score" in request.metadata:
                    score = request.metadata["score"]
                    if isinstance(score, (int, float)) and 0 <= score <= 100:
                        progress.quiz_score = int(score)

            # Set time spent if provided
            if request.metadata and "time_spent" in request.metadata:
                time_spent = request.metadata["time_spent"]
                if isinstance(time_spent, int) and time_spent >= 0:
                    progress.time_spent_seconds = time_spent

            db.add(progress)

        await db.commit()
        logger.info(f"Progress tracked for user {user_id}, chapter {request.chapter_id}, action {action}")

        return TrackProgressResponse(
            success=True,
            progress_updated=now.isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tracking progress: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Failed to track progress"}
        )
