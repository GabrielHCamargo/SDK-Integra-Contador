"""Pydantic models for authentication."""

from typing import Any

from pydantic import BaseModel, Field, field_validator


class AuthCredentials(BaseModel):
    """Model for authentication credentials."""

    consumer_key: str = Field(..., description="Consumer key (API key)")
    consumer_secret: str = Field(..., description="Consumer secret (API secret)")

    @field_validator("consumer_key", "consumer_secret")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """Validate that credentials are not empty."""
        if not v or not v.strip():
            raise ValueError("Consumer key and secret cannot be empty")
        return v.strip()


class CertificateConfig(BaseModel):
    """Model for certificate configuration."""

    path: str = Field(..., description="Path to the certificate file (.p12)")
    password: str = Field(..., description="Certificate password")

    @field_validator("path")
    @classmethod
    def validate_path_format(cls, v: str) -> str:
        """Validate certificate path format."""
        from pathlib import Path

        if not v or not v.strip():
            raise ValueError("Certificate path cannot be empty")
        
        cert_path = Path(v)
        # Resolve to absolute path if possible, but don't check existence yet
        # (file might be created later)
        try:
            return str(cert_path.resolve())
        except (OSError, RuntimeError):
            # If we can't resolve (e.g., path doesn't exist yet), return normalized path
            return str(cert_path)


class TokenResponse(BaseModel):
    """Model for successful token response."""

    expires_in: int = Field(..., description="Token expiration time in seconds")
    scope: str = Field(..., description="Token scope")
    token_type: str = Field(..., description="Token type (should be 'Bearer')")
    access_token: str = Field(..., description="Access token")
    jwt_token: str = Field(..., description="JWT token")
    jwt_pucomex: str | None = Field(
        default=None, description="JWT PuComex token (optional)"
    )

    @field_validator("token_type")
    @classmethod
    def validate_token_type(cls, v: str) -> str:
        """Validate that token type is Bearer."""
        if v.lower() != "bearer":
            raise ValueError(f"Expected token_type to be 'Bearer', got: {v}")
        return v


class AuthErrorResponse(BaseModel):
    """Model for authentication error response."""

    timestamp: str = Field(..., description="Error timestamp")
    status: int = Field(..., description="HTTP status code")
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: list[Any] = Field(default_factory=list, description="Error details")
    trackerId: str | None = Field(default=None, description="Error tracker ID")
    path: str = Field(..., description="API path where error occurred")


class SavedAuthConfig(BaseModel):
    """Model for saved authentication configuration."""

    consumer_key: str = Field(..., description="Consumer key (API key)")
    consumer_secret: str = Field(..., description="Consumer secret (API secret)")
    certificate_path: str = Field(..., description="Path to certificate file (.p12)")
    certificate_password: str = Field(..., description="Certificate password")
    environment: str = Field(..., description="Environment (Trial or Production)")
    saved_at: float | None = Field(default=None, description="Timestamp when config was saved")
