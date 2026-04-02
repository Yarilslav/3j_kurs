"""User schemas for request/response validation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Shared fields for user schemas."""

    name: str
    email: str


class UserCreate(UserBase):
    """Schema for user creation."""

    password: str = Field(min_length=6, max_length=72)


class UserUpdate(UserBase):
    """Schema for user updates."""


class UserResponse(UserBase):
    """Schema for user responses."""

    id: int

    # Allow reading from ORM objects.
    model_config = {"from_attributes": True}
