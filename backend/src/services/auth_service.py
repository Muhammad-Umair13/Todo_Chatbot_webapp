"""Authentication service for Phase II Todo Application.

Handles user registration, login, and JWT token generation.
"""
from typing import Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status

from ..models.user import User, UserCreate, UserLogin, UserResponse, TokenResponse, hash_password, verify_password
from ..auth.jwt import create_test_user_token


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def register(session: Session, user_data: UserCreate) -> TokenResponse:
        """Register a new user and return JWT token.

        Args:
            session: Database session
            user_data: User registration data

        Returns:
            TokenResponse with JWT token and user info

        Raises:
            HTTPException: 400 if email already exists
        """
        # Check if email already exists
        stmt = select(User).where(User.email == user_data.email)
        existing = session.exec(stmt).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hash_password(user_data.password)
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create JWT token
        token = create_test_user_token(
            user_id=str(user.id),
            email=user.email,
            name=user.name
        )

        return TokenResponse(
            access_token=token,
            user=UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=user.created_at
            )
        )

    @staticmethod
    def login(session: Session, credentials: UserLogin) -> TokenResponse:
        """Authenticate user and return JWT token.

        Args:
            session: Database session
            credentials: User login credentials

        Returns:
            TokenResponse with JWT token and user info

        Raises:
            HTTPException: 401 if credentials are invalid
        """
        # Find user by email
        stmt = select(User).where(User.email == credentials.email)
        user = session.exec(stmt).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create JWT token
        token = create_test_user_token(
            user_id=str(user.id),
            email=user.email,
            name=user.name
        )

        return TokenResponse(
            access_token=token,
            user=UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=user.created_at
            )
        )

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """Get user by ID.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            User if found, None otherwise
        """
        return session.get(User, user_id)


__all__ = ["AuthService"]
