"""FastAPI authentication dependencies.

Constitution Principle III: JWT required on protected routes.
Better Auth is the authentication authority (external).

This module provides FastAPI dependencies for extracting and
validating user identity from JWT tokens.
"""
from typing import Optional, Generator
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from .jwt import (
    JWTVerifier,
    UserIdentity,
    TokenPayload,
    TokenValidationError,
    JWTErrorCode,
    get_verifier,
    verify_token,
)
from ..core.config import get_settings


# HTTP Bearer scheme for JWT authentication
security = HTTPBearer(
    scheme_name="Bearer",
    description="JWT token obtained from Better Auth"
)


class AuthenticationError(Exception):
    """Authentication error with structured error details."""

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        headers: Optional[dict] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.headers = headers or {"WWW-Authenticate": "Bearer"}
        super().__init__(self.message)


class AuthenticatedUser(BaseModel):
    """Authenticated user returned by dependency injection.

    This model contains the minimal user information needed by
    downstream services and route handlers.
    """

    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None

    @classmethod
    def from_identity(cls, identity: UserIdentity) -> "AuthenticatedUser":
        """Create AuthenticatedUser from UserIdentity."""
        return cls(
            user_id=identity.user_id,
            email=identity.email,
            name=identity.name,
        )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> AuthenticatedUser:
    """FastAPI dependency to get the current authenticated user.

    This dependency extracts the JWT from the Authorization header,
    validates it, and returns the user identity.

    Usage:
        @router.get("/protected")
        async def protected_route(user: AuthenticatedUser = Depends(get_current_user)):
            return {"user_id": user.user_id}

    Args:
        credentials: HTTP Bearer credentials from Authorization header

    Returns:
        AuthenticatedUser with user information

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "missing_token",
                "message": "Authorization header is required"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        # Verify the token and get user identity
        identity = get_verifier().get_user_identity(token)
        return AuthenticatedUser.from_identity(identity)

    except TokenValidationError as e:
        # Map validation errors to appropriate HTTP responses
        error_response = {
            "error": e.error_code,
            "message": e.message
        }

        # Different status codes based on error type
        if e.error_code in (JWTErrorCode.EXPIRED_TOKEN,):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response,
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif e.error_code in (JWTErrorCode.MISSING_TOKEN,):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response,
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response,
                headers={"WWW-Authenticate": "Bearer"},
            )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[AuthenticatedUser]:
    """FastAPI dependency to optionally get the current user.

    Unlike get_current_user, this does not raise an error if no
    authentication is provided. Returns None instead.

    Usage:
        @router.get("/items")
        async def list_items(user: Optional[AuthenticatedUser] = Depends(get_optional_user)):
            if user:
                return {"items": get_user_items(user.user_id)}
            else:
                return {"items": get_public_items()}

    Args:
        credentials: Optional HTTP Bearer credentials

    Returns:
        AuthenticatedUser if valid token provided, None otherwise
    """
    if credentials is None:
        return None

    token = credentials.credentials

    try:
        identity = get_verifier().get_user_identity(token)
        return AuthenticatedUser.from_identity(identity)
    except TokenValidationError:
        return None


async def require_user_id(
    user: AuthenticatedUser = Depends(get_current_user)
) -> str:
    """FastAPI dependency to extract just the user_id.

    This is a convenience dependency when you only need the user_id
    and not the full user object.

    Usage:
        @router.post("/tasks")
        async def create_task(
            task_data: TaskCreate,
            user_id: str = Depends(require_user_id)
        ):
            return task_service.create(task_data, user_id)

    Args:
        user: AuthenticatedUser from get_current_user

    Returns:
        str: The user's ID
    """
    return user.user_id


class AuthContext(BaseModel):
    """Authentication context for the current request.

    This provides a complete view of the authentication state
    including raw token claims for advanced use cases.
    """

    user: AuthenticatedUser
    token_payload: Optional[TokenPayload] = None
    is_authenticated: bool = True


async def get_auth_context(
    user: AuthenticatedUser = Depends(get_current_user)
) -> AuthContext:
    """FastAPI dependency to get the full authentication context.

    Provides access to both the authenticated user and raw token claims.

    Usage:
        @router.get("/profile")
        async def get_profile(
            context: AuthContext = Depends(get_auth_context)
        ):
            return {
                "user_id": context.user.user_id,
                "email": context.user.email,
                "is_authenticated": context.is_authenticated
            }

    Args:
        user: AuthenticatedUser from get_current_user

    Returns:
        AuthContext with full authentication details
    """
    return AuthContext(user=user)


def create_test_user_token(
    user_id: str,
    email: Optional[str] = None,
    name: Optional[str] = None,
    expires_in: int = 3600
) -> str:
    """Create a JWT token for testing.

    Args:
        user_id: User identifier to include in token
        email: Optional email to include
        name: Optional name to include
        expires_in: Token expiration in seconds

    Returns:
        JWT token string for testing
    """
    settings = get_settings()
    return JWTVerifier.create_test_token(
        secret=settings.jwt_secret,
        user_id=user_id,
        email=email,
        name=name,
        expires_in=expires_in
    )


__all__ = [
    "security",
    "AuthenticationError",
    "AuthenticatedUser",
    "AuthContext",
    "get_current_user",
    "get_optional_user",
    "require_user_id",
    "get_auth_context",
    "create_test_user_token",
]
