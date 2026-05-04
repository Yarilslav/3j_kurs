from __future__ import annotations

from pydantic import BaseModel, Field

from app.models.user import UserRole


class UserRegistration(BaseModel):
    """Public schema for self-registration."""

    name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=3, max_length=255)
    login: str = Field(min_length=1, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    password: str = Field(min_length=6, max_length=72)

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Asahi Guest",
                "email": "guest@example.com",
                "login": "asahi-guest",
                "phone_number": "+380501234567",
                "password": "654321",
            }
        }
    }


class UserCreate(UserRegistration):
    """Internal schema for full user creation."""

    address: str | None = Field(default=None, max_length=255)
    view_history: str | None = None
    purchase_history: str | None = None
    about_employee: str | None = None


class UserBase(BaseModel):
    """Shared fields for user response schemas."""

    name: str
    email: str
    login: str
    phone_number: str | None = None
    address: str | None = None
    view_history: str | None = None
    purchase_history: str | None = None
    about_employee: str | None = None


class UserUpdate(BaseModel):
    """Schema for user updates."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = Field(default=None, min_length=3, max_length=255)
    login: str | None = Field(default=None, min_length=1, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=255)
    view_history: str | None = None
    purchase_history: str | None = None
    about_employee: str | None = None


class UserRoleUpdate(BaseModel):
    """Schema for admin role updates."""

    role: UserRole


class UserResponse(UserBase):
    """Schema for user responses."""

    id: int
    role: UserRole
    bonus_points: int
    model_config = {"from_attributes": True}
