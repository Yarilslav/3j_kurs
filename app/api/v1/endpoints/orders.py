from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_optional_current_user, get_staff_or_admin_user
from app.crud import crud_order
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_optional_current_user),
):
    if current_user is None and (not order.guest_name or not order.guest_contact):
        raise HTTPException(status_code=400, detail="Guest name and contact are required")
    try:
        return await crud_order.create_order(db, order, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=list[OrderResponse])
async def get_orders(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await crud_order.get_orders_for_user(db, current_user)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    _staff=Depends(get_staff_or_admin_user),
):
    order = await crud_order.get_order_by_id(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return await crud_order.update_order_status(db, order, payload.status)
