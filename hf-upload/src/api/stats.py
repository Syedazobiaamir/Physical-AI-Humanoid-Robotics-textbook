"""
Platform Statistics API endpoints

Provides platform-wide statistics for the landing page including:
- Number of books/courses
- Active user count
- Total AI interactions
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..utils.logger import logger

router = APIRouter()


class PlatformStatsResponse(BaseModel):
    """Response schema for platform statistics"""
    books_count: int
    active_users: int
    ai_interactions: int
    chapters_count: int
    updated_at: str


class StatsSummaryResponse(BaseModel):
    """Detailed statistics summary"""
    platform: PlatformStatsResponse
    features: dict
    last_updated: str


# In-memory stats cache (would be replaced with database in production)
# These values can be updated by other services
_stats_cache = {
    "books_count": 1,  # Physical AI Textbook
    "active_users": 0,
    "ai_interactions": 0,
    "chapters_count": 0,
    "updated_at": datetime.utcnow().isoformat()
}


def increment_ai_interactions(count: int = 1) -> None:
    """
    Increment the AI interactions counter.
    Called by RAG and personalization services.
    """
    global _stats_cache
    _stats_cache["ai_interactions"] += count
    _stats_cache["updated_at"] = datetime.utcnow().isoformat()


def update_active_users(count: int) -> None:
    """
    Update the active users count.
    Called by authentication service.
    """
    global _stats_cache
    _stats_cache["active_users"] = count
    _stats_cache["updated_at"] = datetime.utcnow().isoformat()


def update_chapters_count(count: int) -> None:
    """
    Update the chapters count.
    Called by content indexing service.
    """
    global _stats_cache
    _stats_cache["chapters_count"] = count
    _stats_cache["updated_at"] = datetime.utcnow().isoformat()


@router.get("/", response_model=PlatformStatsResponse)
async def get_platform_stats():
    """
    Get platform-wide statistics for the landing page.

    Returns counts for:
    - **books_count**: Number of textbooks/courses on the platform
    - **active_users**: Number of active registered users
    - **ai_interactions**: Total AI skill invocations (chat, personalize, translate)
    - **chapters_count**: Total number of chapters across all books
    - **updated_at**: Last statistics update timestamp
    """
    try:
        return PlatformStatsResponse(
            books_count=_stats_cache["books_count"],
            active_users=_stats_cache["active_users"],
            ai_interactions=_stats_cache["ai_interactions"],
            chapters_count=_stats_cache["chapters_count"],
            updated_at=_stats_cache["updated_at"]
        )
    except Exception as e:
        logger.error(f"Error fetching platform stats: {str(e)}")
        # Return default stats on error
        return PlatformStatsResponse(
            books_count=1,
            active_users=0,
            ai_interactions=0,
            chapters_count=0,
            updated_at=datetime.utcnow().isoformat()
        )


@router.get("/summary", response_model=StatsSummaryResponse)
async def get_stats_summary():
    """
    Get detailed statistics summary.

    Includes platform stats plus feature-specific information.
    """
    try:
        platform_stats = PlatformStatsResponse(
            books_count=_stats_cache["books_count"],
            active_users=_stats_cache["active_users"],
            ai_interactions=_stats_cache["ai_interactions"],
            chapters_count=_stats_cache["chapters_count"],
            updated_at=_stats_cache["updated_at"]
        )

        # Feature statistics
        features = {
            "personalization": {
                "enabled": True,
                "strategies": ["beginner", "hardware_focused", "advanced", "default"]
            },
            "translation": {
                "enabled": True,
                "supported_languages": ["en", "ur"]
            },
            "chatbot": {
                "enabled": True,
                "modes": ["general", "selection"]
            },
            "skills": {
                "available": [
                    "simplify_for_beginner",
                    "hardware_mapping",
                    "context_selection",
                    "exam_ready_summary",
                    "real_world_robot_example"
                ]
            }
        }

        return StatsSummaryResponse(
            platform=platform_stats,
            features=features,
            last_updated=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Error fetching stats summary: {str(e)}")
        return StatsSummaryResponse(
            platform=PlatformStatsResponse(
                books_count=1,
                active_users=0,
                ai_interactions=0,
                chapters_count=0,
                updated_at=datetime.utcnow().isoformat()
            ),
            features={},
            last_updated=datetime.utcnow().isoformat()
        )


@router.post("/increment-interactions")
async def increment_interactions():
    """
    Increment the AI interactions counter.

    This endpoint is called internally by other services
    when an AI skill is invoked.
    """
    increment_ai_interactions(1)
    return {"success": True, "ai_interactions": _stats_cache["ai_interactions"]}
