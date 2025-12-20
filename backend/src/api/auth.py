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

    Note: This is a legacy endpoint. For production use, Clerk authentication is recommended.
    """
    provider = get_oauth_provider(request.provider)

    if not provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "invalid_provider", "message": f"Unsupported OAuth provider: {request.provider}"}
        )

    # Check if provider is configured - ALWAYS check for OAuth credentials
    has_method = hasattr(provider, 'is_configured')
    is_configured = provider.is_configured() if has_method else True
    logger.info(f"OAuth check: provider={request.provider}, has_method={has_method}, is_configured={is_configured}")

    if has_method and not is_configured:
        logger.warning(f"OAuth not configured for {request.provider}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "oauth_not_configured",
                "message": f"{request.provider.title()} OAuth is not configured. Please use Clerk authentication (Sign In button) or configure OAuth credentials.",
                "recommendation": "Use Clerk authentication - it's already set up and ready to use."
            }
        )

    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = {"redirect_uri": request.redirect_uri, "provider": request.provider}

    try:
        auth_url = provider.get_authorization_url(request.redirect_uri, state)
        logger.info(f"OAuth login initiated for provider: {request.provider}")
        return {"auth_url": auth_url}
    except ValueError as e:
        logger.warning(f"OAuth not configured: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "oauth_not_configured", "message": str(e)}
        )
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


# =======================
# Clerk Webhook Handlers
# =======================

# Clerk webhook secret for signature verification
import os
import json
import hmac
import hashlib
from fastapi import Request, Header

CLERK_WEBHOOK_SECRET = os.getenv("CLERK_WEBHOOK_SECRET", "")


class ClerkWebhookRequest(BaseModel):
    """Clerk webhook request payload"""
    data: dict
    object: str
    type: str


class ClerkUserData(BaseModel):
    """Clerk user data from webhook"""
    id: str
    email_addresses: list
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    image_url: Optional[str] = None
    username: Optional[str] = None


def verify_clerk_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verify Clerk webhook signature using HMAC-SHA256
    """
    if not secret:
        logger.warning("Clerk webhook secret not configured")
        return True  # Allow in development without secret

    try:
        expected = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(f"sha256={expected}", signature)
    except Exception as e:
        logger.error(f"Signature verification error: {str(e)}")
        return False


@router.post("/webhook/clerk")
async def clerk_webhook(
    request: Request,
    svix_id: Optional[str] = Header(None, alias="svix-id"),
    svix_timestamp: Optional[str] = Header(None, alias="svix-timestamp"),
    svix_signature: Optional[str] = Header(None, alias="svix-signature"),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle Clerk webhook events for user synchronization

    Supported events:
    - user.created: Create new user in database
    - user.updated: Update existing user
    - user.deleted: Remove user from database

    Clerk sends webhooks with Svix signatures for verification.
    """
    try:
        # Get raw payload for signature verification
        payload = await request.body()

        # Verify signature if secret is configured
        if CLERK_WEBHOOK_SECRET and svix_signature:
            # Build the signed content
            signed_content = f"{svix_id}.{svix_timestamp}.{payload.decode('utf-8')}"

            if not verify_clerk_signature(signed_content.encode('utf-8'), svix_signature, CLERK_WEBHOOK_SECRET):
                logger.warning("Invalid Clerk webhook signature")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid webhook signature"
                )

        # Parse the webhook payload
        data = json.loads(payload)
        event_type = data.get("type", "")
        event_data = data.get("data", {})

        logger.info(f"Received Clerk webhook: {event_type}")

        if event_type == "user.created":
            # Create new user from Clerk data
            clerk_user_id = event_data.get("id")
            email_addresses = event_data.get("email_addresses", [])
            primary_email = next(
                (e.get("email_address") for e in email_addresses if e.get("id") == event_data.get("primary_email_address_id")),
                email_addresses[0].get("email_address") if email_addresses else None
            )

            if not primary_email:
                logger.warning(f"No email found for Clerk user {clerk_user_id}")
                return {"status": "skipped", "reason": "no_email"}

            # Check if user already exists
            result = await db.execute(select(User).where(User.id == clerk_user_id))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                logger.info(f"User {clerk_user_id} already exists, updating")
                existing_user.email = primary_email
                existing_user.name = f"{event_data.get('first_name', '')} {event_data.get('last_name', '')}".strip() or primary_email.split("@")[0]
                existing_user.avatar_url = event_data.get("image_url")
                await db.commit()
                return {"status": "updated", "user_id": clerk_user_id}

            # Create new user
            user = User(
                id=clerk_user_id,  # Use Clerk user ID as primary key
                email=primary_email,
                name=f"{event_data.get('first_name', '')} {event_data.get('last_name', '')}".strip() or primary_email.split("@")[0],
                role=UserRole.STUDENT.value,
                oauth_provider="clerk",
                oauth_id=clerk_user_id,
                avatar_url=event_data.get("image_url")
            )
            db.add(user)
            await db.commit()
            logger.info(f"Created user from Clerk: {primary_email}")
            return {"status": "created", "user_id": clerk_user_id}

        elif event_type == "user.updated":
            # Update existing user
            clerk_user_id = event_data.get("id")
            result = await db.execute(select(User).where(User.id == clerk_user_id))
            user = result.scalar_one_or_none()

            if not user:
                logger.warning(f"User {clerk_user_id} not found for update")
                return {"status": "not_found"}

            email_addresses = event_data.get("email_addresses", [])
            primary_email = next(
                (e.get("email_address") for e in email_addresses if e.get("id") == event_data.get("primary_email_address_id")),
                None
            )

            if primary_email:
                user.email = primary_email
            user.name = f"{event_data.get('first_name', '')} {event_data.get('last_name', '')}".strip() or user.name
            user.avatar_url = event_data.get("image_url") or user.avatar_url

            await db.commit()
            logger.info(f"Updated user from Clerk: {clerk_user_id}")
            return {"status": "updated", "user_id": clerk_user_id}

        elif event_type == "user.deleted":
            # Delete user
            clerk_user_id = event_data.get("id")
            result = await db.execute(select(User).where(User.id == clerk_user_id))
            user = result.scalar_one_or_none()

            if user:
                await db.delete(user)
                await db.commit()
                logger.info(f"Deleted user from Clerk webhook: {clerk_user_id}")
                return {"status": "deleted", "user_id": clerk_user_id}
            else:
                return {"status": "not_found"}

        else:
            logger.debug(f"Unhandled Clerk event type: {event_type}")
            return {"status": "ignored", "event_type": event_type}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Clerk webhook error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook processing failed"
        )
