from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password
from app.crud import crud_user
from app.schemas.user import UserCreate


async def ensure_root_admin(db: AsyncSession) -> None:
    if not settings.ADMIN_BOOTSTRAP_ENABLED:
        return

    admin = UserCreate(
        name=settings.ADMIN_NAME,
        email=settings.ADMIN_EMAIL,
        login=settings.ADMIN_LOGIN,
        phone_number=settings.ADMIN_PHONE_NUMBER,
        address=None,
        view_history=None,
        purchase_history=None,
        about_employee=None,
        password=settings.ADMIN_PASSWORD,
    )

    await crud_user.upsert_bootstrap_admin(
        db=db,
        user_in=admin,
        hashed_password=hash_password(settings.ADMIN_PASSWORD),
    )
