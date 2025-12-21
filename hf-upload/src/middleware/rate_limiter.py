"""
Rate limiting middleware for API protection
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
import os
from typing import Dict, Tuple

# Rate limit configuration
RATE_LIMIT_PER_HOUR = int(os.getenv("RATE_LIMIT_PER_HOUR", "100"))
RATE_LIMIT_UNAUTH_PER_HOUR = int(os.getenv("RATE_LIMIT_UNAUTH_PER_HOUR", "10"))


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware to prevent API abuse
    """

    def __init__(self, app):
        super().__init__(app)
        # Store request counts: {identifier: (count, reset_time)}
        self.request_counts: Dict[str, Tuple[int, datetime]] = defaultdict(
            lambda: (0, datetime.utcnow() + timedelta(hours=1))
        )

    def _get_identifier(self, request: Request) -> str:
        """Get unique identifier for rate limiting (user ID or IP)"""
        # Try to get user ID from token
        auth_header = request.headers.get("authorization")
        if auth_header:
            # In production, decode JWT and extract user ID
            # For now, use the token as identifier
            return f"user_{auth_header}"

        # Fall back to IP address for unauthenticated requests
        client_ip = request.client.host if request.client else "unknown"
        return f"ip_{client_ip}"

    def _is_authenticated(self, request: Request) -> bool:
        """Check if request has valid authentication"""
        return request.headers.get("authorization") is not None

    def _get_rate_limit(self, is_authenticated: bool) -> int:
        """Get rate limit based on authentication status"""
        return RATE_LIMIT_PER_HOUR if is_authenticated else RATE_LIMIT_UNAUTH_PER_HOUR

    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting"""
        identifier = self._get_identifier(request)
        is_authenticated = self._is_authenticated(request)
        rate_limit = self._get_rate_limit(is_authenticated)

        # Get current count and reset time
        count, reset_time = self.request_counts[identifier]

        # Check if we need to reset the counter
        now = datetime.utcnow()
        if now >= reset_time:
            count = 0
            reset_time = now + timedelta(hours=1)

        # Increment counter
        count += 1
        self.request_counts[identifier] = (count, reset_time)

        # Check if rate limit exceeded
        if count > rate_limit:
            remaining_time = int((reset_time - now).total_seconds())
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "rate_limited",
                    "message": "Too many requests. Please try again later.",
                    "retry_after": remaining_time
                },
                headers={
                    "X-RateLimit-Limit": str(rate_limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(reset_time.timestamp())),
                    "Retry-After": str(remaining_time)
                }
            )

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(rate_limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, rate_limit - count))
        response.headers["X-RateLimit-Reset"] = str(int(reset_time.timestamp()))

        return response
