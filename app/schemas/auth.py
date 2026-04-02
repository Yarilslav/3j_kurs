"""Authentication request/response schemas."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Schema for user login."""

    login: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=72)


class TokenResponse(BaseModel):
    """Schema for access token responses."""

    access_token: str
    token_type: str = "bearer"
