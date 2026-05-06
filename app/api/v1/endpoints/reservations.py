from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_optional_current_user, get_staff_or_admin_user
from app.crud import crud_reservation
from app.db.session import get_db
from app.schemas.reservation import ReservationCreate, ReservationResponse, ReservationStatusUpdate

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation: ReservationCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_optional_current_user),
):
    if current_user is None and (not reservation.guest_name or not reservation.guest_contact):
        raise HTTPException(status_code=400, detail="Guest name and contact are required")
    return await crud_reservation.create_reservation(db, reservation, current_user)


@router.get("/", response_model=list[ReservationResponse])
async def get_reservations(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await crud_reservation.get_reservations_for_user(db, current_user)


@router.patch("/{reservation_id}/status", response_model=ReservationResponse)
async def update_reservation_status(
    reservation_id: int,
    payload: ReservationStatusUpdate,
    db: AsyncSession = Depends(get_db),
    _staff=Depends(get_staff_or_admin_user),
):
    reservation = await crud_reservation.get_reservation_by_id(db, reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return await crud_reservation.update_reservation_status(db, reservation, payload.status)
