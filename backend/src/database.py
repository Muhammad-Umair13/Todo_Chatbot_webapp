"""Database connection and session management.

Constitution Principle IX: No secrets in code. Database URL from
environment variables via pydantic-settings (config.py).

Constitution Principle IV: SQLModel ORM only, no raw SQL queries.
"""
from typing import Generator
from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session
from loguru import logger

# Import settings (environment variables)
from .core.config import get_settings

settings = get_settings()

# Create SQLModel engine for Neon PostgreSQL
# Connection pooling with pool_pre_ping ensures stale connections are detected
# before use, preventing connection errors in long-running applications
engine = create_engine(
    settings.database_url,
    echo=settings.environment.lower() == "development",
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for obtaining a database session.

    This function provides a clean session management pattern for dependency injection.
    Sessions are automatically created and closed after each request.

    Yields:
        Session: A SQLModel session for database operations.

    Example:
        ```python
        from fastapi import Depends
        from src.database import get_session

        @app.get("/api/tasks")
        def get_tasks(session: Session = Depends(get_session)):
            tasks = session.exec(select(Task)).all()
            return tasks
        ```

    Notes:
        - Sessions are context managers that handle cleanup automatically.
        - No manual commit/rollback in this layer - handled by business logic.
        - Each request gets its own session for proper isolation.
    """
    with Session(engine) as session:
        try:
            yield session
        finally:
            # Session is automatically closed by context manager
            # This ensures no connection leaks
            pass


def get_engine():
    """
    Get a database engine instance.

    This is useful for Alembic migrations and database initialization.

    Returns:
        Engine: The SQLAlchemy engine instance.

    Example:
        ```python
        from src.database import get_engine
        from sqlmodel import SQLModel
        engine = get_engine()
        SQLModel.metadata.create_all(engine)
        ```

    Notes:
        - The same engine is reused across all database operations.
        - Connection pooling is configured at engine creation.
    """
    return engine


def close_engine() -> None:
    """
    Close all database connections in the engine pool.

    This should be called during application shutdown to ensure proper cleanup.
    FastAPI's lifespan context manager is a recommended place to call this.

    Example:
        ```python
        from fastapi import FastAPI
        from src.database import close_engine

        app = FastAPI()

        @app.on_event("shutdown")
        def shutdown_event():
            close_engine()
        ```
    """
    logger.info("Closing database engine connections...")
    engine.dispose()
    logger.info("Database engine closed")


__all__ = ["get_session", "get_engine", "close_engine", "engine", "SQLModel"]
