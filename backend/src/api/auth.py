"""
Authentication API endpoints for OAuth and JWT handling
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional
import uuid
import secrets

from ..database.base import get_db
from ..auth.oauth import get_oauth_provider
from ..auth.jwt_handler import create_access_token, create_refresh_token, verify_token
from ..models.user import User, UserRole
from ..utils.logger import logger

router = APIRouter()


# Pydantic Schemas
class OAuthLoginRequest(BaseModel):
    """OAuth login initiation request"""
    provider: str = Field(..., description="OAuth provider: 'google' or 'github'")
    redirect_uri: str = Field(..., description="Redirect URI after OAuth flow")


class OAuthLoginResponse(BaseModel):
    """OAuth login initiation response"""
    auth_url: str


class OAuthCallbackRequest(BaseModel):
    """OAuth callback request"""
    code: str = Field(..., description="Authorization code from OAuth provider")
    provider: str = Field(..., description="OAuth provider: 'google' or 'github'")
    redirect_uri: Optional[str] = Field(None, description="Original redirect URI")


class UserResponse(BaseModel):
    """User information response"""
    id: str
    email: str
    name: str
    role: str
    avatar_url: Optional[str] = None
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None


class OAuthCallbackResponse(BaseModel):
    """OAuth callback response with tokens"""
    access_token: str
    refresh_token: str
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Token refresh request"""
    refresh_token: str = Field(..., description="Valid refresh token")


class RefreshTokenResponse(BaseModel):
    """Token refresh response"""
    access_token: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    message: Optional[str] = None


# State storage for OAuth CSRF protection (in production, use Redis or database)
_oauth_states: dict = {}


@router.post("/login/oauth", response_model=OAuthLoginResponse)
async def oauth_login(request: OAuthLoginRequest):
    """
    Initiate OAuth login flow with supported providers

    - **provider**: OAuth provider to use ('google' or 'github')
    - **redirect_uri**: URI to redirect to after OAuth completion
    """
    provider = get_oauth_provider(request.provider)

    if not provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_provider", "message": f"Unsupported OAuth provider: {request.provider}"}
        )

    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = {"redirect_uri": request.redirect_uri, "provider": request.provider}

    try:
        auth_url = provider.get_authorization_url(request.redirect_uri, state)
        logger.info(f"OAuth login initiated for provider: {request.provider}")
        return {"auth_url": auth_url}
    except Exception as e:
        logger.error(f"Error generating OAuth URL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "oauth_error", "message": "Failed to generate OAuth URL"}
        )


@router.post("/login/callback", response_model=OAuthCallbackResponse)
async def oauth_callback(
    request: OAuthCallbackRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Handle OAuth callback and return JWT tokens

    - **code**: Authorization code from OAuth provider
    - **provider**: OAuth provider that completed the flow
    """
    provider = get_oauth_provider(request.provider)

    if not provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_provider", "message": f"Unsupported OAuth provider: {request.provider}"}
        )

    try:
        # Get redirect_uri from request or use default
        redirect_uri = request.redirect_uri or "http://localhost:3000/auth/callback"

        # Exchange code for access token
        oauth_token = await provider.get_access_token(request.code, redirect_uri)

        if not oauth_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "invalid_code", "message": "Failed to exchange authorization code"}
            )

        # Get user info from OAuth provider
        user_info = await provider.get_user_info(oauth_token)

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "authentication_failed", "message": "Failed to retrieve user information"}
            )

        # Extract user data based on provider
        if request.provider.lower() == "google":
            email = user_info.get("email")
            name = user_info.get("name", email.split("@")[0])
            oauth_id = user_info.get("id")
            avatar_url = user_info.get("picture")
        elif request.provider.lower() == "github":
            email = user_info.get("email")
            name = user_info.get("name") or user_info.get("login", "")
            oauth_id = str(user_info.get("id"))
            avatar_url = user_info.get("avatar_url")
        else:
            email = user_info.get("email")
            name = user_info.get("name", "")
            oauth_id = user_info.get("id")
            avatar_url = None

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "missing_email", "message": "Email not provided by OAuth provider"}
            )

        # Find or create user
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            # Create new user
            user = User(
                id=str(uuid.uuid4()),
                email=email,
                name=name,
                role=UserRole.STUDENT.value,
                oauth_provider=request.provider.lower(),
                oauth_id=oauth_id,
                avatar_url=avatar_url
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            logger.info(f"New user created via OAuth: {email}")
        else:
            # Update existing user OAuth info if needed
            if not user.oauth_provider:
                user.oauth_provider = request.provider.lower()
                user.oauth_id = oauth_id
            if avatar_url:
                user.avatar_url = avatar_url
            await db.commit()
            logger.info(f"Existing user logged in via OAuth: {email}")

        # Create JWT tokens
        token_data = user.to_jwt_payload()
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                role=user.role,
                avatar_url=user.avatar_url,
                software_background=user.software_background,
                hardware_background=user.hardware_background
            )
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OAuth callback error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "authentication_failed", "message": "OAuth authentication failed"}
        )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using a valid refresh token

    - **refresh_token**: Valid JWT refresh token
    """
    payload = verify_token(request.refresh_token, token_type="refresh")

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "invalid_token", "message": "Invalid or expired refresh token"}
        )

    try:
        # Verify user still exists
        user_id = payload.get("sub")
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "invalid_token", "message": "User no longer exists"}
            )

        # Create new access token
        token_data = user.to_jwt_payload()
        access_token = create_access_token(token_data)

        logger.info(f"Access token refreshed for user: {user.email}")
        return {"access_token": access_token}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "refresh_failed", "message": "Failed to refresh token"}
        )
