from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


async def get_products(db: AsyncSession) -> list[Product]:

    result = await db.execute(select(Product).options(selectinload(Product.categories)).order_by(Product.id))
    return result.scalars().unique().all()


async def get_product_by_id(db: AsyncSession, product_id: int) -> Product | None:

    result = await db.execute(
        select(Product).options(selectinload(Product.categories)).where(Product.id == product_id)
    )
    return result.scalars().unique().first()


async def get_products_by_ids(db: AsyncSession, product_ids: Sequence[int]) -> list[Product]:

    result = await db.execute(
        select(Product).options(selectinload(Product.categories)).where(Product.id.in_(product_ids))
    )
    return result.scalars().unique().all()


async def get_product_count(db: AsyncSession) -> int:

    result = await db.execute(select(func.count()).select_from(Product))
    return result.scalar_one()


async def _get_or_create_categories(db: AsyncSession, category_names: list[str]) -> list[Category]:

    normalized_names = list(dict.fromkeys(name.strip() for name in category_names if name.strip()))
    if not normalized_names:
        return []

    existing_result = await db.execute(select(Category).where(Category.name.in_(normalized_names)))
    existing = {category.name: category for category in existing_result.scalars().all()}
    categories = list(existing.values())

    for name in normalized_names:
        if name not in existing:
            category = Category(name=name)
            db.add(category)
            categories.append(category)

    await db.flush()
    categories.sort(key=lambda category: normalized_names.index(category.name))
    return categories


async def create_product(db: AsyncSession, product_in: ProductCreate) -> Product:

    categories = await _get_or_create_categories(db, product_in.categories)
    product = Product(
        name=product_in.name,
        native_name=product_in.native_name,
        image_filename=product_in.image_filename,
        kind=product_in.kind,
        description=product_in.description,
        price_uah=product_in.price_uah,
        stock_quantity=product_in.stock_quantity,
        reviews=None,
        categories=categories,
    )
    db.add(product)
    await db.commit()
    return await get_product_by_id(db, product.id)


async def update_product(db: AsyncSession, product: Product, product_in: ProductUpdate) -> Product:

    updates = product_in.model_dump(exclude_unset=True)
    category_names = updates.pop("categories", None)

    for field_name, value in updates.items():
        setattr(product, field_name, value)

    if category_names is not None:
        product.categories = await _get_or_create_categories(db, category_names)

    await db.commit()
    return await get_product_by_id(db, product.id)


async def delete_product(db: AsyncSession, product: Product) -> None:

    await db.delete(product)
    await db.commit()
