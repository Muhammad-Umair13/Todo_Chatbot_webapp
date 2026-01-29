"""Auth router with authentication endpoints.

Constitution Principle III: JWT required on protected routes.
Better Auth is the authentication authority (external).

This module provides:
- Login and registration endpoints for local authentication
- Protected endpoints that demonstrate JWT authentication
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from .dependencies import (
    AuthenticatedUser,
    AuthContext,
    get_current_user,
    get_optional_user,
    get_auth_context,
    require_user_id,
)
from .jwt import create_test_user_token
from ..database import get_session
from ..models.user import UserCreate, UserLogin, TokenResponse
from ..services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: Session = Depends(get_session)
) -> TokenResponse:
    """Register a new user account.

    Creates a new user with the provided email, name, and password.
    Returns a JWT token for immediate authentication.

    Args:
        user_data: User registration data (email, name, password)
        session: Database session

    Returns:
        TokenResponse with access_token and user information

    Raises:
        HTTPException: 400 if email is already registered
    """
    return AuthService.register(session, user_data)


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    session: Session = Depends(get_session)
) -> TokenResponse:
    """Authenticate user and return JWT token.

    Validates user credentials and returns a JWT token for API access.

    Args:
        credentials: User login credentials (email, password)
        session: Database session

    Returns:
        TokenResponse with access_token and user information

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    return AuthService.login(session, credentials)


@router.get("/me", response_model=AuthenticatedUser)
async def get_current_user_info(
    user: AuthenticatedUser = Depends(get_current_user)
) -> AuthenticatedUser:
    """Get the currently authenticated user's information.

    Requires a valid JWT token in the Authorization header.

    Returns:
        AuthenticatedUser with user_id, email, and name

    Example:
        Authorization: Bearer <token>

        Response:
        {
            "user_id": "user-123",
            "email": "user@example.com",
            "name": "John Doe"
        }
    """
    return user


@router.get("/me/context", response_model=dict)
async def get_auth_context_info(
    context: AuthContext = Depends(get_auth_context)
) -> dict:
    """Get the full authentication context for the current request.

    Requires a valid JWT token in the Authorization header.

    Returns:
        Dict with user info and authentication status
    """
    return {
        "user_id": context.user.user_id,
        "email": context.user.email,
        "name": context.user.name,
        "is_authenticated": context.is_authenticated,
        "token_claims": context.user.token_claims
    }


@router.get("/user-id")
async def get_user_id(user_id: str = Depends(require_user_id)) -> dict:
    """Get just the user ID of the authenticated user.

    Convenience endpoint when you only need the user_id.

    Returns:
        Dict with user_id
    """
    return {"user_id": user_id}


@router.get("/optional")
async def optional_user_info(
    user: AuthenticatedUser = Depends(get_optional_user)
) -> dict:
    """Get user info if authenticated, or None if not.

    Unlike other endpoints, this does NOT require authentication.
    Returns null user if no token is provided.

    Returns:
        Dict with user info or null
    """
    if user:
        return {
            "authenticated": True,
            "user_id": user.user_id,
            "email": user.email,
            "name": user.name
        }
    return {
        "authenticated": False,
        "user_id": None,
        "email": None,
        "name": None
    }


@router.post("/test-token")
async def create_test_token(
    user_id: str,
    email: str = None,
    name: str = None,
    expires_in: int = 3600
) -> dict:
    """Create a test JWT token for development purposes.

    WARNING: This endpoint is for development/testing only.
    Never use in production!

    Args:
        user_id: User identifier for the token
        email: Optional email claim
        name: Optional name claim
        expires_in: Token expiration in seconds (default: 1 hour)

    Returns:
        Dict with the generated token
    """
    token = create_test_user_token(
        user_id=user_id,
        email=email,
        name=name,
        expires_in=expires_in
    )
    return {
        "token": token,
        "type": "Bearer",
        "expires_in": expires_in
    }


__all__ = ["router"]
