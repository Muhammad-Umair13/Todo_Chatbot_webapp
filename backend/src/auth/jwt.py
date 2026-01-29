"""JWT verification utilities for Phase II Todo Application.

Constitution Principle III: JWT required on protected routes.
Better Auth is the authentication authority (external).

This module provides stateless JWT verification without user storage.
All user identity comes from the JWT token claims.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError


class TokenValidationError(Exception):
    """Raised when JWT token validation fails."""

    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class JWTErrorCode(str, Enum):
    """Error codes for JWT validation failures."""

    MISSING_TOKEN = "missing_token"
    INVALID_TOKEN = "invalid_token"
    EXPIRED_TOKEN = "expired_token"
    INVALID_SIGNATURE = "invalid_signature"
    INVALID_CLAIMS = "invalid_claims"
    MISSING_USER_ID = "missing_user_id"
    INVALID_ALGORITHM = "invalid_algorithm"


class TokenPayload(BaseModel):
    """JWT token payload model.

    This represents the claims extracted from a valid JWT token.
    The 'sub' claim is required and contains the user_id.
    """

    sub: str = Field(
        ...,
        description="Subject claim (user identifier from Better Auth)",
        examples=["user-123", "auth0|abc123"]
    )
    exp: Optional[int] = Field(
        default=None,
        description="Expiration time (Unix timestamp)",
        examples=[1705315200]
    )
    iat: Optional[int] = Field(
        default=None,
        description="Issued at time (Unix timestamp)",
        examples=[1705311600]
    )
    iss: Optional[str] = Field(
        default=None,
        description="Issuer claim",
        examples=["better-auth"]
    )
    aud: Optional[str] = Field(
        default=None,
        description="Audience claim",
        examples=["todo-api"]
    )
    # Additional claims that Better Auth might include
    email: Optional[str] = Field(
        default=None,
        description="User email address"
    )
    email_verified: Optional[bool] = Field(
        default=None,
        description="Whether email is verified"
    )
    name: Optional[str] = Field(
        default=None,
        description="User display name"
    )
    picture: Optional[str] = Field(
        default=None,
        description="User profile picture URL"
    )

    class Config:
        extra = "allow"  # Allow additional claims


class UserIdentity(BaseModel):
    """Authenticated user identity extracted from JWT.

    This is the canonical representation of the user in the backend.
    All database queries use user_id from this model to enforce ownership.
    """

    user_id: str = Field(
        ...,
        description="Unique user identifier (from JWT sub claim)",
        examples=["user-123"]
    )
    email: Optional[str] = Field(
        default=None,
        description="User email address if available"
    )
    name: Optional[str] = Field(
        default=None,
        description="User display name if available"
    )
    token_claims: Dict[str, Any] = Field(
        default_factory=dict,
        description="Raw token claims for advanced use cases"
    )

    @classmethod
    def from_payload(cls, payload: TokenPayload) -> "UserIdentity":
        """Create UserIdentity from a validated TokenPayload."""
        return cls(
            user_id=payload.sub,
            email=payload.email,
            name=payload.name,
            token_claims=payload.model_dump(exclude_none=True)
        )


class JWTVerifier:
    """Stateless JWT verification utility.

    This class handles all JWT validation without storing any user state.
    All validation is stateless and based solely on token content.

    Usage:
        verifier = JWTVerifier()
        payload = verifier.verify(token)
        user = UserIdentity.from_payload(payload)
    """

    def __init__(
        self,
        secret: str,
        algorithm: str = "HS256",
        audience: Optional[str] = None,
        issuer: Optional[str] = None,
    ):
        """Initialize the JWT verifier.

        Args:
            secret: Secret key for verifying HS256 signatures
            algorithm: Expected algorithm (default: HS256)
            audience: Expected audience claim (optional)
            issuer: Expected issuer claim (optional)
        """
        self.secret = secret
        self.algorithm = algorithm
        self.audience = audience
        self.issuer = issuer
        self._allowed_algorithms = {"HS256", "HS384", "HS512", "RS256", "RS384", "RS512"}

    def verify(self, token: str) -> TokenPayload:
        """Verify and decode a JWT token.

        Args:
            token: The JWT token string (Bearer token)

        Returns:
            TokenPayload with validated claims

        Raises:
            TokenValidationError: If token is invalid, expired, or claims are invalid
        """
        if not token:
            raise TokenValidationError(
                "Token is missing or empty",
                JWTErrorCode.MISSING_TOKEN
            )

        try:
            # Build options for JWT decoding
            options = {
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
                "require": ["sub", "exp"],  # Require subject and expiration
                "clock_skew_leeway": 10,  # 10-second clock tolerance for time differences
            }

            if self.audience:
                options["verify_aud"] = True
                options["audience"] = self.audience
            else:
                options["verify_aud"] = False

            if self.issuer:
                options["verify_iss"] = True
                options["issuer"] = self.issuer
            else:
                options["verify_iss"] = False

            # Decode and verify the token
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
                options=options
            )

            # Validate required claims
            if not payload.get("sub"):
                raise TokenValidationError(
                    "Token missing required 'sub' claim (user identifier)",
                    JWTErrorCode.MISSING_USER_ID
                )

            # Create and return the payload model
            return TokenPayload(**payload)

        except ExpiredSignatureError:
            raise TokenValidationError(
                "Token has expired",
                JWTErrorCode.EXPIRED_TOKEN
            )
        except JWTClaimsError as e:
            raise TokenValidationError(
                f"Token claims validation failed: {str(e)}",
                JWTErrorCode.INVALID_CLAIMS
            )
        except JWTError as e:
            # Generic JWT errors (signature, etc.)
            error_msg = str(e).lower()
            if "signature" in error_msg or "verify" in error_msg:
                raise TokenValidationError(
                    "Token signature verification failed",
                    JWTErrorCode.INVALID_SIGNATURE
                )
            elif "algorithm" in error_msg:
                raise TokenValidationError(
                    "Token uses invalid algorithm",
                    JWTErrorCode.INVALID_ALGORITHM
                )
            else:
                raise TokenValidationError(
                    f"Token validation failed: {str(e)}",
                    JWTErrorCode.INVALID_TOKEN
                )

    def get_user_identity(self, token: str) -> UserIdentity:
        """Verify token and extract user identity in one call.

        Args:
            token: The JWT token string

        Returns:
            UserIdentity with user information

        Raises:
            TokenValidationError: If token is invalid
        """
        payload = self.verify(token)
        return UserIdentity.from_payload(payload)

    @staticmethod
    def create_test_token(
        secret: str,
        user_id: str,
        algorithm: str = "HS256",
        expires_in: int = 3600,
        email: Optional[str] = None,
        name: Optional[str] = None,
        **extra_claims: Any
    ) -> str:
        """Create a JWT token for testing purposes.

        Args:
            secret: Secret key for signing
            user_id: User identifier (sub claim)
            algorithm: Algorithm to use (default: HS256)
            expires_in: Expiration time in seconds (default: 1 hour)
            email: Optional email claim
            name: Optional name claim
            **extra_claims: Additional claims to include

        Returns:
            Signed JWT token string
        """
        now = int(datetime.now().timestamp())  # Use consistent timestamp method
        exp = now + expires_in

        claims = {
            "sub": user_id,
            "iat": now,
            "exp": exp,
            **extra_claims
        }

        if email:
            claims["email"] = email
        if name:
            claims["name"] = name

        return jwt.encode(claims, secret, algorithm=algorithm)


# Module-level verifier instance (lazy initialization)
_verifier: Optional[JWTVerifier] = None


def get_verifier() -> JWTVerifier:
    """Get the module-level JWT verifier instance.

    This lazy-initializes the verifier with settings from config.

    Returns:
        JWTVerifier instance configured from environment

    Raises:
        ValueError: If JWT_SECRET is not configured
    """
    global _verifier
    if _verifier is None:
        from ..core.config import get_settings
        settings = get_settings()

        if not settings.jwt_secret:
            raise ValueError("JWT_SECRET must be configured in environment")

        _verifier = JWTVerifier(
            secret=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
            audience=getattr(settings, "jwt_audience", None),
            issuer=getattr(settings, "jwt_issuer", None),
        )
    return _verifier


def verify_token(token: str) -> TokenPayload:
    """Verify a JWT token and return its payload.

    This is a convenience function that uses the module-level verifier.

    Args:
        token: JWT token string

    Returns:
        TokenPayload with validated claims

    Raises:
        TokenValidationError: If token is invalid
    """
    return get_verifier().verify(token)


def get_user_identity(token: str) -> UserIdentity:
    """Verify token and extract user identity.

    Args:
        token: JWT token string

    Returns:
        UserIdentity with user information

    Raises:
        TokenValidationError: If token is invalid
    """
    return get_verifier().get_user_identity(token)


def create_test_user_token(
    user_id: str,
    email: Optional[str] = None,
    name: Optional[str] = None,
    expires_in: int = 3600
) -> str:
    """Create a JWT token for user authentication.

    This is used for local authentication (login/register flows).
    The token includes user_id as the 'sub' claim for ownership enforcement.

    Args:
        user_id: User identifier (will be used as 'sub' claim)
        email: Optional email claim
        name: Optional name claim
        expires_in: Token expiration in seconds (default: 1 hour)

    Returns:
        Signed JWT token string
    """
    from ..core.config import get_settings
    settings = get_settings()

    return JWTVerifier.create_test_token(
        secret=settings.jwt_secret,
        user_id=user_id,
        algorithm=settings.jwt_algorithm,
        expires_in=expires_in,
        email=email,
        name=name,
        iss=settings.jwt_issuer,
        aud=settings.jwt_audience,
    )


__all__ = [
    "TokenValidationError",
    "JWTErrorCode",
    "TokenPayload",
    "UserIdentity",
    "JWTVerifier",
    "get_verifier",
    "verify_token",
    "get_user_identity",
    "create_test_user_token",
]
