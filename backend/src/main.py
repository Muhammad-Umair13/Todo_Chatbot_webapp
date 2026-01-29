"""
Main FastAPI application module.

Phase II: Full-Stack Multi-User Web Todo Application
Constitution Principle III: JWT required on protected routes.
Better Auth is the authentication authority (external).
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from loguru import logger

from .core.config import settings
from .core.security import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    setup_security_error_handlers,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager for startup and shutdown events.

    Startup:
        - Initializes logging and configuration validation
        - Database connection is established lazily on first request

    Shutdown:
        - Closes database engine connections gracefully
    """
    # Startup
    logger.info("Starting up Phase II Todo API...")
    logger.info(f"Environment: {settings.environment}")

    # Hide credentials for database URLs that have them (skip for sqlite)
    db_display = settings.database_url
    if '@' in settings.database_url:
        db_display = settings.database_url.split('@')[1]
    logger.info(f"Database configured: {db_display}")  # Hide credentials

    logger.info(f"CORS origins: {settings.cors_origins}")
    yield
    # Shutdown
    from .database import close_engine
    close_engine()
    logger.info("Phase II Todo API shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Phase II Todo API",
    description="Full-Stack Multi-User Web Todo Application - Backend API. "
                "JWT authentication required on protected routes.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add custom exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Setup security error handlers for auth errors
setup_security_error_handlers(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for load balancers and monitoring."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/api/v1/health")
async def api_health_check() -> dict[str, str]:
    """API versioned health check endpoint."""
    return {"status": "healthy", "version": "1.0.0", "environment": settings.environment}


# Import and include routers
from .routers import tasks
from .auth.router import router as auth_router
from .chatbot import chat_router  # Phase III: AI Chatbot (from chatbot package)

app.include_router(tasks.router)
app.include_router(auth_router)
app.include_router(chat_router)  # Phase III: AI Chatbot endpoints


__all__ = ["app"]
