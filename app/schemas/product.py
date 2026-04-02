"""Product schemas for response validation."""

from __future__ import annotations

from pydantic import BaseModel


class ProductResponse(BaseModel):
    """Schema for product responses."""

    id: int
    name: str
    description: str | None
    image_path: str | None
    steepness_index: float
    category_id: int

    # Allow reading from ORM objects.
    model_config = {"from_attributes": True}
