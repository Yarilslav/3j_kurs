from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.reservation import ReservationStatus


def _normalize_places(value: list[int] | str) -> list[int]:
    if isinstance(value, str):
        items = [part.strip() for part in value.split(",")]
        value = [int(item) for item in items if item]
    if not value:
        raise ValueError("At least one place is required")
    return value


class ReservationCreate(BaseModel):
    reservation_at: str = Field(min_length=1, max_length=255)
    places: list[int] | str
    guest_name: str | None = Field(default=None, max_length=255)
    guest_contact: str | None = Field(default=None, max_length=255)

    @field_validator("places")
    @classmethod
    def validate_places(cls, value: list[int] | str) -> list[int]:
        return _normalize_places(value)

    @model_validator(mode="after")
    def validate_guest_fields(self):
        if self.guest_name is None and self.guest_contact is None:
            return self
        if not self.guest_name or not self.guest_contact:
            raise ValueError("Both guest_name and guest_contact are required for guest reservations")
        return self


class ReservationStatusUpdate(BaseModel):
    status: ReservationStatus


class ReservationResponse(BaseModel):
    id: int
    user_id: int | None
    guest_name: str | None
    guest_contact: str | None
    reservation_at: str
    places: list[int]
    status: ReservationStatus
    price: int

    model_config = {"from_attributes": True}

    @field_validator("places", mode="before")
    @classmethod
    def parse_places(cls, value):
        if isinstance(value, str):
            return [int(item) for item in value.split(",") if item]
        return value
