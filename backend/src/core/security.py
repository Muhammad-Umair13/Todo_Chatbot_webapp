"""Security error handlers for FastAPI.

Constitution Principle III: JWT required on protected routes.
Better Auth is the authentication authority (external).

This module provides centralized error handling for authentication
and authorization failures.
"""
from fastapi import Request, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Any

from ..auth.dependencies import AuthenticationError
from ..auth.jwt import TokenValidationError, JWTErrorCode


class SecurityError(Exception):
    """Base security error with structured details."""

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 401,
        details: dict = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class UnauthorizedError(SecurityError):
    """Raised when authentication is required but not provided."""

    def __init__(self, message: str = "Authentication required", details: dict = None):
        super().__init__(
            message=message,
            error_code="unauthorized",
            status_code=401,
            details=details
        )


class ForbiddenError(SecurityError):
    """Raised when user is authenticated but lacks permission."""

    def __init__(self, message: str = "Access denied", details: dict = None):
        super().__init__(
            message=message,
            error_code="forbidden",
            status_code=403,
            details=details
        )


def format_auth_error(error: TokenValidationError) -> dict:
    """Format a TokenValidationError for HTTP response.

    Args:
        error: The token validation error

    Returns:
        Dict formatted for JSON response
    """
    response = {
        "error": error.error_code,
        "message": error.message
    }

    # Add helpful hints based on error type
    if error.error_code == JWTErrorCode.EXPIRED_TOKEN:
        response["hint"] = "Your session has expired. Please log in again."
    elif error.error_code == JWTErrorCode.INVALID_SIGNATURE:
        response["hint"] = "Token signature is invalid. Please log in again."
    elif error.error_code == JWTErrorCode.MISSING_TOKEN:
        response["hint"] = "Include a valid Bearer token in the Authorization header."
    elif error.error_code == JWTErrorCode.INVALID_TOKEN:
        response["hint"] = "The provided token is malformed or invalid."

    return response


def format_security_error(error: SecurityError) -> dict:
    """Format a SecurityError for HTTP response.

    Args:
        error: The security error

    Returns:
        Dict formatted for JSON response
    """
    response = {
        "error": error.error_code,
        "message": error.message
    }

    if error.details:
        response["details"] = error.details

    return response


class AuthErrorMiddleware(BaseHTTPMiddleware):
    """Middleware to catch and format authentication errors.

    This middleware intercepts AuthenticationError and TokenValidationError
    exceptions and returns properly formatted JSON responses.
    """

    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except TokenValidationError as e:
            # JWT validation errors from auth dependencies
            status_code = 401
            if e.error_code == JWTErrorCode.EXPIRED_TOKEN:
                status_code = 401
            elif e.error_code == JWTErrorCode.MISSING_TOKEN:
                status_code = 401

            return JSONResponse(
                status_code=status_code,
                content=format_auth_error(e),
                headers={"WWW-Authenticate": "Bearer"}
            )

        except AuthenticationError as e:
            # Custom auth errors from dependencies
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": e.error_code,
                    "message": e.message
                },
                headers=e.headers
            )

        except SecurityError as e:
            # General security errors
            return JSONResponse(
                status_code=e.status_code,
                content=format_security_error(e)
            )


def setup_security_error_handlers(app: FastAPI) -> None:
    """Register security error handlers with the FastAPI app.

    Args:
        app: FastAPI application instance
    """
    # Add middleware for catching exceptions
    app.add_middleware(AuthErrorMiddleware)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPException with structured error format.

    Args:
        request: The incoming request
        exc: The HTTPException

    Returns:
        JSONResponse with formatted error
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": str(exc.detail) if exc.detail else "An error occurred",
            "status_code": exc.status_code
        },
        headers=exc.headers
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle RequestValidationError with detailed error messages.

    Args:
        request: The incoming request
        exc: The validation error

    Returns:
        JSONResponse with validation error details
    """
    errors = []
    for error in exc.errors():
        loc = " -> ".join(str(l) for l in error.get("loc", []))
        msg = error.get("msg", "")
        errors.append(f"{loc}: {msg}")

    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Request validation failed",
            "details": errors
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle uncaught exceptions with generic error response.

    Args:
        request: The incoming request
        exc: The uncaught exception

    Returns:
        JSONResponse with generic error (hides internal details)
    """
    # Log the full error server-side
    import traceback
    print(f"Unhandled exception: {exc}")
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "An internal error occurred"
        }
    )


__all__ = [
    "SecurityError",
    "UnauthorizedError",
    "ForbiddenError",
    "format_auth_error",
    "format_security_error",
    "AuthErrorMiddleware",
    "setup_security_error_handlers",
    "http_exception_handler",
    "validation_exception_handler",
    "general_exception_handler",
]
