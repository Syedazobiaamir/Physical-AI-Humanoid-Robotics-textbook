"""
Content API endpoints for textbook chapters
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel, Field
from ..database.base import get_db
from ..services.content_service import ContentService
from ..utils.errors import NotFoundError
from ..utils.logger import logger

router = APIRouter()


# Pydantic schemas
class ChapterResponse(BaseModel):
    """Chapter response schema"""
    id: str
    title: str
    module: str
    week: int
    learning_objectives: List[str]
    content: str
    code_examples: List[dict] = []
    lab_tasks: List[dict] = []
    resources: List[dict] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ChapterDetailResponse(BaseModel):
    """Detailed chapter response with navigation"""
    chapter: ChapterResponse
    next_chapter: Optional[str] = None
    prev_chapter: Optional[str] = None


class ChaptersListResponse(BaseModel):
    """List of chapters response"""
    chapters: List[ChapterResponse]
    total: int


@router.get("/chapters", response_model=ChaptersListResponse)
async def get_chapters(
    module: Optional[str] = Query(None, description="Filter by module"),
    week_from: Optional[int] = Query(None, description="Filter by week range (start)", ge=1, le=13),
    week_to: Optional[int] = Query(None, description="Filter by week range (end)", ge=1, le=13),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all chapters with optional filters

    - **module**: Filter by module (e.g., "Module 1")
    - **week_from**: Filter by week range start
    - **week_to**: Filter by week range end
    """
    try:
        service = ContentService(db)
        chapters = await service.get_chapters(
            module=module,
            week_from=week_from,
            week_to=week_to
        )

        return {
            "chapters": [ChapterResponse(**chapter.to_dict()) for chapter in chapters],
            "total": len(chapters)
        }
    except Exception as e:
        logger.error(f"Error in get_chapters endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chapters"
        )


@router.get("/chapters/{chapter_id}", response_model=ChapterDetailResponse)
async def get_chapter(
    chapter_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific chapter content with navigation links

    - **chapter_id**: Unique chapter identifier
    """
    try:
        service = ContentService(db)
        chapter = await service.get_chapter_by_id(chapter_id)

        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chapter not found: {chapter_id}"
            )

        # Get next and previous chapters
        next_chapter = await service.get_next_chapter(chapter_id)
        prev_chapter = await service.get_previous_chapter(chapter_id)

        return {
            "chapter": ChapterResponse(**chapter.to_dict()),
            "next_chapter": next_chapter.id if next_chapter else None,
            "prev_chapter": prev_chapter.id if prev_chapter else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_chapter endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chapter"
        )


# SDK Content Schemas
class SDKExample(BaseModel):
    """SDK code example"""
    name: str
    description: str
    language: str
    file_path: str
    code: Optional[str] = None


class SDKContentResponse(BaseModel):
    """SDK content for a chapter"""
    sdk_examples: List[SDKExample]
    repository_links: List[dict]


# Chapter to SDK examples mapping
CHAPTER_SDK_MAPPING = {
    "week-1-intro": {
        "examples": [
            {
                "name": "Basic Publisher Node",
                "description": "A simple ROS2 publisher that sends messages to a topic",
                "language": "python",
                "file_path": "sdk-examples/ros2-basics/publisher_node.py"
            },
            {
                "name": "Basic Subscriber Node",
                "description": "A simple ROS2 subscriber that receives messages from a topic",
                "language": "python",
                "file_path": "sdk-examples/ros2-basics/subscriber_node.py"
            }
        ],
        "repository_links": [
            {
                "name": "ROS2 Examples",
                "url": "https://github.com/ros2/examples",
                "description": "Official ROS2 example packages"
            }
        ]
    },
    "week-5-computer-vision": {
        "examples": [
            {
                "name": "Object Detector Node",
                "description": "ROS2 node for object detection using camera images",
                "language": "python",
                "file_path": "sdk-examples/perception/object_detector.py"
            }
        ],
        "repository_links": [
            {
                "name": "vision_opencv",
                "url": "https://github.com/ros-perception/vision_opencv",
                "description": "OpenCV integration for ROS2"
            }
        ]
    },
    "week-9-control": {
        "examples": [
            {
                "name": "PID Controller Node",
                "description": "Implementation of a PID controller for robot joint control",
                "language": "python",
                "file_path": "sdk-examples/control/pid_controller.py"
            }
        ],
        "repository_links": [
            {
                "name": "ros2_control",
                "url": "https://github.com/ros-controls/ros2_control",
                "description": "ROS2 control framework"
            }
        ]
    }
}


@router.get("/chapters/{chapter_id}/sdk-content", response_model=SDKContentResponse)
async def get_sdk_content(chapter_id: str):
    """
    Get SDK code examples for a specific chapter

    - **chapter_id**: Unique chapter identifier

    Returns associated SDK code examples and repository links.
    """
    try:
        # Get SDK content for chapter
        sdk_data = CHAPTER_SDK_MAPPING.get(chapter_id)

        if not sdk_data:
            # Return empty content for chapters without SDK examples
            return {
                "sdk_examples": [],
                "repository_links": []
            }

        # Build response
        examples = []
        for example in sdk_data.get("examples", []):
            sdk_example = SDKExample(
                name=example["name"],
                description=example["description"],
                language=example["language"],
                file_path=example["file_path"],
                code=None  # Code can be loaded on demand from frontend
            )
            examples.append(sdk_example)

        return {
            "sdk_examples": examples,
            "repository_links": sdk_data.get("repository_links", [])
        }

    except Exception as e:
        logger.error(f"Error in get_sdk_content endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve SDK content"
        )
