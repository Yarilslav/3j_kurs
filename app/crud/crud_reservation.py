from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reservation import Reservation, ReservationStatus
from app.models.user import User, UserRole
from app.schemas.reservation import ReservationCreate


async def get_reservations_for_user(db: AsyncSession, current_user: User) -> list[Reservation]:

    statement = select(Reservation).order_by(Reservation.id)
    if current_user.role not in {UserRole.STAFF, UserRole.ADMIN}:
        statement = statement.where(Reservation.user_id == current_user.id)
    result = await db.execute(statement)
    return result.scalars().all()


async def get_reservation_by_id(db: AsyncSession, reservation_id: int) -> Reservation | None:

    result = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    return result.scalars().first()


async def create_reservation(
    db: AsyncSession,
    reservation_in: ReservationCreate,
    current_user: User | None,
) -> Reservation:

    reservation = Reservation(
        user_id=current_user.id if current_user is not None else None,
        guest_name=None if current_user is not None else reservation_in.guest_name,
        guest_contact=None if current_user is not None else reservation_in.guest_contact,
        reservation_at=reservation_in.reservation_at,
        places=",".join(str(place) for place in reservation_in.places),
        status=ReservationStatus.PENDING,
        price=0,
    )
    db.add(reservation)
    await db.commit()
    return await get_reservation_by_id(db, reservation.id)


async def update_reservation_status(
    db: AsyncSession,
    reservation: Reservation,
    status: ReservationStatus,
) -> Reservation:

    reservation.status = status
    await db.commit()
    return await get_reservation_by_id(db, reservation.id)
