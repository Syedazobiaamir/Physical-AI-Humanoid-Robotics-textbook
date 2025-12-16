"""
User Profile API endpoints

Handles user profile operations including:
- Creating/updating user profiles with background information
- Retrieving user profile data
- Managing personalization preferences
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from ..database.base import get_db
from ..models.user import User
from ..utils.logger import logger

router = APIRouter()


# Pydantic Schemas
class UserProfileCreate(BaseModel):
    """Request schema for creating/updating user profile"""
    software_level: str = Field(
        default="beginner",
        description="Software skill level: beginner, intermediate, advanced"
    )
    hardware_exposure: str = Field(
        default="none",
        description="Hardware exposure: none, some, extensive"
    )
    robotics_experience: str = Field(
        default="none",
        description="Robotics experience: none, some, extensive"
    )
    language_preference: str = Field(
        default="en",
        description="Language preference: en, ur"
    )
    learning_goals: Optional[List[str]] = Field(
        default=None,
        description="List of learning goals"
    )


class UserProfileResponse(BaseModel):
    """Response schema for user profile"""
    id: str
    email: str
    name: str
    software_level: Optional[str] = None
    hardware_exposure: Optional[str] = None
    robotics_experience: Optional[str] = None
    language_preference: str = "en"
    learning_goals: Optional[List[str]] = None
    avatar_url: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """Request schema for updating specific profile fields"""
    name: Optional[str] = None
    software_level: Optional[str] = None
    hardware_exposure: Optional[str] = None
    robotics_experience: Optional[str] = None
    language_preference: Optional[str] = None
    learning_goals: Optional[List[str]] = None


# Helper to get current user (placeholder - would integrate with Clerk in production)
async def get_current_user_id(
    # In production, this would verify Clerk JWT
    # For now, accept user_id as header or query param
    user_id: Optional[str] = None
) -> Optional[str]:
    """Get current user ID from auth context"""
    return user_id


@router.post("/profile", response_model=UserProfileResponse)
async def create_or_update_profile(
    profile_data: UserProfileCreate,
    user_id: str,  # Would come from Clerk JWT in production
    db: AsyncSession = Depends(get_db)
):
    """
    Create or update user profile with background information

    This endpoint is called after user signup to collect:
    - software_level: Programming experience level
    - hardware_exposure: Electronics/hardware experience
    - robotics_experience: Prior robotics experience
    - language_preference: Preferred content language
    - learning_goals: User's learning objectives
    """
    try:
        # Find existing user
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update profile fields
        user.software_background = profile_data.software_level
        user.hardware_background = profile_data.hardware_exposure

        # Store additional profile data in a JSON field if available
        # For now, we'll use the existing fields
        if profile_data.language_preference:
            # Would store in user_profiles table in production
            pass

        await db.commit()
        await db.refresh(user)

        logger.info(f"Profile updated for user: {user_id}")

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            software_level=user.software_background,
            hardware_exposure=user.hardware_background,
            robotics_experience=profile_data.robotics_experience,
            language_preference=profile_data.language_preference,
            learning_goals=profile_data.learning_goals,
            avatar_url=user.avatar_url,
            created_at=user.created_at.isoformat() if user.created_at else datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating/updating profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.get("/profile/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user profile by ID

    Returns the user's profile including personalization preferences.
    """
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            software_level=user.software_background,
            hardware_exposure=user.hardware_background,
            robotics_experience=None,  # Would come from user_profiles table
            language_preference="en",  # Would come from user_profiles table
            learning_goals=None,  # Would come from user_profiles table
            avatar_url=user.avatar_url,
            created_at=user.created_at.isoformat() if user.created_at else datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch profile"
        )


@router.patch("/profile/{user_id}", response_model=UserProfileResponse)
async def update_profile_fields(
    user_id: str,
    update_data: UserProfileUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update specific profile fields

    Allows partial updates to user profile without requiring all fields.
    """
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update only provided fields
        if update_data.name is not None:
            user.name = update_data.name
        if update_data.software_level is not None:
            user.software_background = update_data.software_level
        if update_data.hardware_exposure is not None:
            user.hardware_background = update_data.hardware_exposure

        await db.commit()
        await db.refresh(user)

        logger.info(f"Profile fields updated for user: {user_id}")

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            software_level=user.software_background,
            hardware_exposure=user.hardware_background,
            robotics_experience=update_data.robotics_experience,
            language_preference=update_data.language_preference or "en",
            learning_goals=update_data.learning_goals,
            avatar_url=user.avatar_url,
            created_at=user.created_at.isoformat() if user.created_at else datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile fields: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.get("/me")
async def get_current_user_profile(
    user_id: str,  # Would come from Clerk JWT in production
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated user's profile

    Convenience endpoint that returns the profile of the currently
    authenticated user based on their JWT token.
    """
    return await get_user_profile(user_id, db)
