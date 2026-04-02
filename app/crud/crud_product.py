"""Product CRUD operations using SQLAlchemy AsyncSession."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


async def get_products(db: AsyncSession) -> list[Product]:
    """Return all products."""

    result = await db.execute(select(Product))
    return result.scalars().all()
