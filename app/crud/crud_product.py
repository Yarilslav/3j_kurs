from __future__ import annotations
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product


async def get_products(db: AsyncSession) -> list[Product]:

    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_product_count(db: AsyncSession) -> int:

    result = await db.execute(select(func.count()).select_from(Product))
    return result.scalar_one()
