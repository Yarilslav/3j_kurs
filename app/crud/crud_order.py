from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.models.user import User, UserRole
from app.schemas.order import OrderCreate


def _format_what_ordered(order_items: list[OrderItem], products_by_id: dict[int, Product]) -> str:
    return ", ".join(
        f"{products_by_id[item.product_id].name} x{item.quantity}"
        for item in order_items
    )


async def get_orders_for_user(db: AsyncSession, current_user: User) -> list[Order]:

    statement = select(Order).options(selectinload(Order.items)).order_by(Order.id)
    if current_user.role not in {UserRole.STAFF, UserRole.ADMIN}:
        statement = statement.where(Order.user_id == current_user.id)
    result = await db.execute(statement)
    return result.scalars().unique().all()


async def get_order_by_id(db: AsyncSession, order_id: int) -> Order | None:

    result = await db.execute(select(Order).options(selectinload(Order.items)).where(Order.id == order_id))
    return result.scalars().unique().first()


async def create_order(db: AsyncSession, order_in: OrderCreate, current_user: User | None) -> Order:

    product_ids = [item.product_id for item in order_in.items]
    products = await db.execute(select(Product).where(Product.id.in_(product_ids)).order_by(Product.id))
    products_list = products.scalars().all()
    products_by_id = {product.id: product for product in products_list}

    if len(products_by_id) != len(set(product_ids)):
        raise ValueError("One or more products were not found")

    order_items: list[OrderItem] = []
    total_price = 0
    for item in order_in.items:
        product = products_by_id[item.product_id]
        if product.stock_quantity < item.quantity:
            raise ValueError(f"Not enough stock for product {product.id}")
        line_total = product.price_uah * item.quantity
        total_price += line_total
        product.stock_quantity -= item.quantity
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price_uah,
                line_total=line_total,
            )
        )

    order = Order(
        user_id=current_user.id if current_user is not None else None,
        guest_name=None if current_user is not None else order_in.guest_name,
        guest_contact=None if current_user is not None else order_in.guest_contact,
        address=order_in.address,
        status=OrderStatus.PENDING,
        total_price=total_price,
        what_ordered="",
        items=order_items,
    )
    order.what_ordered = _format_what_ordered(order_items, products_by_id)
    db.add(order)
    await db.commit()
    return await get_order_by_id(db, order.id)


async def update_order_status(db: AsyncSession, order: Order, status: OrderStatus) -> Order:

    order.status = status
    await db.commit()
    return await get_order_by_id(db, order.id)
