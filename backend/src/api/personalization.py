"""
Personalization API endpoints for content adaptation
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

from ..database.base import get_db
from ..auth.dependencies import get_current_user
from ..models.personalization_profile import PersonalizationProfile
from ..models.chapter import Chapter
from ..utils.logger import logger

router = APIRouter()


# Pydantic Schemas
class PreferencesResponse(BaseModel):
    """User preferences response"""
    skill_level: str
    customizations: Dict[str, Any] = {}


class PreferencesUpdateRequest(BaseModel):
    """Update preferences request"""
    skill_level: str = Field(..., description="Skill level: 'beginner', 'intermediate', or 'advanced'")
    customizations: Optional[Dict[str, Any]] = Field(default={}, description="Additional customization options")


class PreferencesUpdateResponse(BaseModel):
    """Update preferences response"""
    success: bool


class AdaptContentRequest(BaseModel):
    """Adapt content request"""
    chapter_id: str = Field(..., description="Chapter ID to adapt content for")
    skill_level: str = Field(..., description="Target skill level: 'beginner', 'intermediate', or 'advanced'")
    content_format: str = Field(default="mdx", description="Output format: 'mdx' or 'html'")


class AdaptContentResponse(BaseModel):
    """Adapted content response"""
    adapted_content: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    message: Optional[str] = None


# Valid skill levels
VALID_SKILL_LEVELS = {"beginner", "intermediate", "advanced"}


@router.get("/preferences/{chapter_id}", response_model=PreferencesResponse)
async def get_preferences(
    chapter_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's personalization preferences for a specific chapter

    - **chapter_id**: Chapter identifier to get preferences for
    """
    user_id = current_user.get("sub")

    try:
        # Find existing preferences
        result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == user_id,
                PersonalizationProfile.chapter_id == chapter_id
            )
        )
        profile = result.scalar_one_or_none()

        if not profile:
            # Return default preferences if not found
            return PreferencesResponse(
                skill_level="intermediate",
                customizations={}
            )

        return PreferencesResponse(
            skill_level=profile.skill_level,
            customizations=profile.customizations or {}
        )

    except Exception as e:
        logger.error(f"Error getting preferences: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Failed to retrieve preferences"}
        )


@router.put("/preferences/{chapter_id}", response_model=PreferencesUpdateResponse)
async def update_preferences(
    chapter_id: str,
    request: PreferencesUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Set user's personalization preferences for a specific chapter

    - **chapter_id**: Chapter identifier to set preferences for
    - **skill_level**: Preferred skill level
    - **customizations**: Additional preferences
    """
    user_id = current_user.get("sub")

    # Validate skill level
    if request.skill_level.lower() not in VALID_SKILL_LEVELS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_preferences", "message": f"Invalid skill level. Must be one of: {', '.join(VALID_SKILL_LEVELS)}"}
        )

    try:
        # Find existing preferences
        result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == user_id,
                PersonalizationProfile.chapter_id == chapter_id
            )
        )
        profile = result.scalar_one_or_none()

        if profile:
            # Update existing profile
            profile.skill_level = request.skill_level.lower()
            profile.customizations = request.customizations or {}
            profile.updated_at = datetime.utcnow()
        else:
            # Create new profile
            import uuid
            profile = PersonalizationProfile(
                id=str(uuid.uuid4()),
                user_id=user_id,
                chapter_id=chapter_id,
                skill_level=request.skill_level.lower(),
                customizations=request.customizations or {}
            )
            db.add(profile)

        await db.commit()
        logger.info(f"Preferences updated for user {user_id}, chapter {chapter_id}")
        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating preferences: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Failed to update preferences"}
        )


@router.post("/adapt-content", response_model=AdaptContentResponse)
async def adapt_content(
    request: AdaptContentRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized content adaptation based on skill level

    - **chapter_id**: Chapter to adapt
    - **skill_level**: Target skill level for adaptation
    - **content_format**: Output format ('mdx' or 'html')
    """
    # Validate skill level
    if request.skill_level.lower() not in VALID_SKILL_LEVELS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_request", "message": f"Invalid skill level. Must be one of: {', '.join(VALID_SKILL_LEVELS)}"}
        )

    # Validate content format
    if request.content_format.lower() not in {"mdx", "html"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_request", "message": "Invalid content format. Must be 'mdx' or 'html'"}
        )

    try:
        # Get chapter content
        result = await db.execute(
            select(Chapter).where(Chapter.id == request.chapter_id)
        )
        chapter = result.scalar_one_or_none()

        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "not_found", "message": f"Chapter not found: {request.chapter_id}"}
            )

        # Adapt content based on skill level
        # For now, we provide different introductory text based on skill level
        # In production, this would integrate with Claude Code subagent for dynamic adaptation
        adapted_content = _adapt_content_for_skill_level(
            chapter.content,
            request.skill_level.lower(),
            chapter.title
        )

        # Convert to HTML if requested
        if request.content_format.lower() == "html":
            # Basic MDX to HTML conversion (in production, use proper MDX parser)
            adapted_content = _mdx_to_basic_html(adapted_content)

        logger.info(f"Content adapted for chapter {request.chapter_id}, skill level {request.skill_level}")
        return {"adapted_content": adapted_content}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adapting content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Failed to adapt content"}
        )


def _adapt_content_for_skill_level(content: str, skill_level: str, title: str) -> str:
    """
    Adapt chapter content for a specific skill level

    This is a simplified implementation. In production, this would
    integrate with Claude Code subagent for dynamic content adaptation.
    """
    skill_intros = {
        "beginner": f""":::info Beginner Mode
**Learning Path for Beginners**

This chapter has been adapted for learners new to {title}. We'll:
- Start with fundamental concepts and definitions
- Provide extra explanations for technical terms
- Include step-by-step walkthroughs for all code examples
- Offer additional practice exercises

Take your time with each section. Don't hesitate to revisit earlier chapters if needed.
:::

""",
        "intermediate": f""":::tip Intermediate Mode
**Building on Your Foundation**

This chapter assumes familiarity with basic concepts. We'll:
- Focus on practical applications
- Dive deeper into implementation details
- Connect concepts to real-world scenarios
- Provide optimization tips and best practices

Feel free to skip sections you're already comfortable with.
:::

""",
        "advanced": f""":::caution Advanced Mode
**Deep Dive Content**

This chapter is optimized for experienced practitioners. We'll:
- Skip basic explanations and focus on advanced topics
- Discuss edge cases and performance considerations
- Explore cutting-edge research and techniques
- Present challenging exercises and projects

Reference materials and research papers are linked throughout.
:::

"""
    }

    intro = skill_intros.get(skill_level, "")
    return intro + content


def _mdx_to_basic_html(mdx_content: str) -> str:
    """
    Basic MDX to HTML conversion

    This is a simplified implementation. In production, use a proper
    MDX parser and renderer.
    """
    import re

    html_content = mdx_content

    # Convert headers
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)

    # Convert bold and italic
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)

    # Convert code blocks
    html_content = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code class="language-\1">\2</code></pre>', html_content, flags=re.DOTALL)

    # Convert inline code
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)

    # Convert admonitions (Docusaurus style)
    html_content = re.sub(r':::info\s*(.+?)\n(.*?):::', r'<div class="admonition info"><div class="admonition-title">\1</div><div class="admonition-content">\2</div></div>', html_content, flags=re.DOTALL)
    html_content = re.sub(r':::tip\s*(.+?)\n(.*?):::', r'<div class="admonition tip"><div class="admonition-title">\1</div><div class="admonition-content">\2</div></div>', html_content, flags=re.DOTALL)
    html_content = re.sub(r':::caution\s*(.+?)\n(.*?):::', r'<div class="admonition caution"><div class="admonition-title">\1</div><div class="admonition-content">\2</div></div>', html_content, flags=re.DOTALL)

    # Convert paragraphs (basic)
    paragraphs = html_content.split('\n\n')
    html_content = '\n'.join(
        f'<p>{p}</p>' if not p.startswith('<') else p
        for p in paragraphs
        if p.strip()
    )

    return f'<div class="adapted-content">\n{html_content}\n</div>'
