"""
Custom exception classes for the application
"""
from typing import Optional, Any


class BaseAPIException(Exception):
    """Base exception for API errors"""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "internal_error",
        details: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)


class AuthenticationError(BaseAPIException):
    """Authentication failed"""

    def __init__(self, message: str = "Authentication failed", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=401,
            error_code="authentication_error",
            details=details
        )


class AuthorizationError(BaseAPIException):
    """Insufficient permissions"""

    def __init__(self, message: str = "Insufficient permissions", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=403,
            error_code="authorization_error",
            details=details
        )


class NotFoundError(BaseAPIException):
    """Resource not found"""

    def __init__(self, message: str = "Resource not found", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=404,
            error_code="not_found",
            details=details
        )


class ValidationError(BaseAPIException):
    """Request validation failed"""

    def __init__(self, message: str = "Validation failed", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="validation_error",
            details=details
        )


class RateLimitError(BaseAPIException):
    """Rate limit exceeded"""

    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=429,
            error_code="rate_limit_error",
            details=details
        )


class ServiceUnavailableError(BaseAPIException):
    """External service unavailable"""

    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        details: Optional[Any] = None
    ):
        super().__init__(
            message=message,
            status_code=503,
            error_code="service_unavailable",
            details=details
        )
