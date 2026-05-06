from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1)
    address: str | None = Field(default=None, max_length=255)
    guest_name: str | None = Field(default=None, max_length=255)
    guest_contact: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def validate_guest_fields(self):
        if self.guest_name is None and self.guest_contact is None:
            return self
        if not self.guest_name or not self.guest_contact:
            raise ValueError("Both guest_name and guest_contact are required for guest orders")
        return self


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: int
    line_total: int

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    user_id: int | None
    guest_name: str | None
    guest_contact: str | None
    status: OrderStatus
    items: list[OrderItemResponse]
    what_ordered: str
    address: str | None
    total_price: int

    model_config = {"from_attributes": True}
