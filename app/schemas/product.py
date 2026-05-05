from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"


def _normalize_categories(value: list[str] | str) -> list[str]:
    if isinstance(value, str):
        items = value.split(",")
    else:
        items = value
    normalized = [item.strip() for item in items if item and item.strip()]
    if not normalized:
        raise ValueError("At least one category is required")
    return normalized


def _validate_image_filename(value: str | None) -> str | None:
    if value is None:
        return None
    file_name = value.strip()
    if not file_name:
        return None
    available = {
        path.name.lower(): path.name
        for path in ASSETS_DIR.rglob("*")
        if path.is_file()
    }
    match = available.get(file_name.lower())
    if match is None:
        raise ValueError("Image file was not found in assets")
    return match


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    native_name: str | None = Field(default=None, max_length=255)
    image_filename: str | None = Field(default=None, max_length=255)
    kind: str = Field(min_length=1, max_length=255)
    description: str | None = None
    price_uah: int = Field(ge=0)
    stock_quantity: int = Field(ge=0)

    @field_validator("image_filename")
    @classmethod
    def validate_image_filename(cls, value: str | None) -> str | None:
        return _validate_image_filename(value)


class ProductCreate(ProductBase):
    categories: list[str] | str

    @field_validator("categories")
    @classmethod
    def validate_categories(cls, value: list[str] | str) -> list[str]:
        return _normalize_categories(value)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    native_name: str | None = Field(default=None, max_length=255)
    image_filename: str | None = Field(default=None, max_length=255)
    kind: str | None = Field(default=None, min_length=1, max_length=255)
    categories: list[str] | str | None = None
    description: str | None = None
    price_uah: int | None = Field(default=None, ge=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    reviews: str | None = None

    @field_validator("image_filename")
    @classmethod
    def validate_image_filename(cls, value: str | None) -> str | None:
        return _validate_image_filename(value)

    @field_validator("categories")
    @classmethod
    def validate_categories(cls, value: list[str] | str | None) -> list[str] | None:
        if value is None:
            return None
        return _normalize_categories(value)


class ProductResponse(ProductBase):
    id: int
    categories: list[str]
    reviews: str | None = None

    model_config = {"from_attributes": True}

    @field_validator("categories", mode="before")
    @classmethod
    def validate_categories(cls, value):
        if isinstance(value, list) and value and hasattr(value[0], "name"):
            return [category.name for category in value]
        return value

    @classmethod
    def from_product(cls, product) -> "ProductResponse":
        return cls(
            id=product.id,
            name=product.name,
            native_name=product.native_name,
            image_filename=product.image_filename,
            kind=product.kind,
            description=product.description,
            price_uah=product.price_uah,
            stock_quantity=product.stock_quantity,
            reviews=product.reviews,
            categories=[category.name for category in product.categories],
        )
