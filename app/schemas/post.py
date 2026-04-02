"""Post schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    """Shared fields for posts."""

    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    """Schema for creating a post."""


class PostResponse(PostBase):
    """Schema for post responses."""

    id: int
    user_id: int

    model_config = {"from_attributes": True}
