"""
Pytest configuration and fixtures.

Phase II: Full-Stack Multi-User Web Todo Application
"""
import asyncio
from datetime import datetime, timezone
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.core.config import settings
from src.models.user import hash_password as get_password_hash
from src.database import get_session, engine
from src.main import app
from src.models.user import User
from src.models.task import Task, Priority


# Create in-memory SQLite engine for testing
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    # Create tables
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def db_session(test_engine) -> Generator[Session, None, None]:
    """Create a test database session."""
    with Session(test_engine) as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client for the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
def client(test_engine) -> Generator[TestClient, None, None]:
    """Create a synchronous test client for the FastAPI app."""
    # Override the database engine
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def clean_db(test_engine):
    """Clean database before each test."""
    # Clear all data
    with Session(test_engine) as session:
        # Delete in reverse order due to foreign key constraints
        session.execute("DELETE FROM tasks")
        session.execute("DELETE FROM users")
        session.commit()
    yield
    # Cleanup after test
    with Session(test_engine) as session:
        session.execute("DELETE FROM tasks")
        session.execute("DELETE FROM users")
        session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_user(test_engine) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        name="Test User",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    with Session(test_engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

    return user


@pytest_asyncio.fixture(scope="function")
async def test_tasks(test_engine, test_user) -> list[Task]:
    """Create test tasks for the test user."""
    tasks = [
        Task(
            user_id=test_user.id,
            title="Test Task 1",
            description="Description for test task 1",
            completed=False,
            priority=Priority.HIGH,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
        Task(
            user_id=test_user.id,
            title="Test Task 2",
            description="Description for test task 2",
            completed=True,
            priority=Priority.LOW,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
    ]

    with Session(test_engine) as session:
        for task in tasks:
            session.add(task)
        session.commit()
        for task in tasks:
            session.refresh(task)

    return tasks


@pytest.fixture
def auth_headers(test_user) -> dict[str, str]:
    """Generate authentication headers for the test user."""
    from src.core.security import create_access_token

    token = create_access_token(data={"sub": str(test_user.id), "email": test_user.email})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def expired_auth_headers(test_user) -> dict[str, str]:
    """Generate expired authentication headers for the test user."""
    from datetime import timedelta

    from src.core.security import create_access_token

    token = create_access_token(
        data={"sub": str(test_user.id), "email": test_user.email},
        expires_delta=timedelta(seconds=-1),  # Already expired
    )
    return {"Authorization": f"Bearer {token}"}


# Configuration for pytest
pytest_plugins = [
    "pytest_asyncio",
]


__all__ = [
    "test_engine",
    "db_session",
    "async_client",
    "client",
    "clean_db",
    "test_user",
    "test_tasks",
    "auth_headers",
    "expired_auth_headers",
]
