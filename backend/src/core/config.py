"""Application configuration using Pydantic Settings.

Constitution Principle IX: No secrets in code - all sensitive data
comes from environment variables.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """Application settings with environment variable support.

    All sensitive values (DATABASE_URL) come from environment
    per Constitution Principle IX - Security & Error Handling.
    """

    # Database connection string (REQUIRED - no default to prevent missing env var)
    database_url: str = Field(
        ...,
        description="PostgreSQL database connection string from Neon",
        alias="DATABASE_URL"  # Allow both DATABASE_URL and database_url
    )

    # JWT configuration for authentication
    jwt_secret: str = Field(
        ...,
        description="Secret key for signing JWT tokens",
        alias="JWT_SECRET"
    )

    jwt_algorithm: str = Field(
        default="HS256",
        description="Algorithm used for JWT signing"
    )

    jwt_audience: str = Field(
        default="todo-api",
        description="Expected audience claim in JWT tokens"
    )

    jwt_issuer: str = Field(
        default="better-auth",
        description="Expected issuer claim in JWT tokens"
    )

    # Application name for logging
    app_name: str = Field(
        default="todo-api",
        description="Application name for structured logging"
    )

    # Log level for development vs production
    log_level: str = Field(
        default="INFO",
        description="Log level (DEBUG, INFO, WARNING, ERROR)"
    )

    # Environment mode
    environment: str = Field(
        default="development",
        description="Environment (development, staging, production)"
    )

    # CORS configuration
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:3001,http://localhost:8000",
        description="Comma-separated list of allowed CORS origins"
    )

    # Phase III: Gemini configuration for AI Chatbot
    gemini_api_key: str = Field(
        default="",
        description="Google Gemini API key for AI chatbot (Phase III)",
        alias="GEMINI_API_KEY"
    )

    gemini_model: str = Field(
        default="gemini-2.0-flash",
        description="Gemini model to use for chat (default: gemini-2.0-flash)",
        alias="GEMINI_MODEL"
    )

    def cors_origins_list(self) -> List[str]:
        """Convert the comma-separated CORS origins string to a list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"  # Load from .env file in backend directory
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance."""
    return settings