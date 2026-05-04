from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate


async def get_users(db: AsyncSession) -> list[User]:

    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user_count(db: AsyncSession) -> int:

    result = await db.execute(select(func.count()).select_from(User))
    return result.scalar_one()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:

    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user_by_login(db: AsyncSession, login: str) -> User | None:

    result = await db.execute(select(User).where(User.login == login))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:

    return await db.get(User, user_id)


async def get_user_by_name(db: AsyncSession, name: str) -> User | None:

    result = await db.execute(select(User).where(User.name == name))
    return result.scalars().first()


async def create_user(
    db: AsyncSession,
    user_in: UserCreate,
    hashed_password: str,
    role: UserRole = UserRole.USER,
) -> User:

    user = User(
        name=user_in.name,
        email=user_in.email,
        login=user_in.login,
        phone_number=user_in.phone_number,
        hashed_password=hashed_password,
        role=role,
        address=user_in.address,
        view_history=user_in.view_history,
        purchase_history=user_in.purchase_history,
        about_employee=user_in.about_employee,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def upsert_bootstrap_admin(
    db: AsyncSession,
    *,
    user_in: UserCreate,
    hashed_password: str,
) -> User:

    user = await get_user_by_login(db, user_in.login)
    if user is None:
        user = await get_user_by_email(db, user_in.email)

    if user is None:
        return await create_user(
            db=db,
            user_in=user_in,
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
        )

    user.name = user_in.name
    user.email = user_in.email
    user.login = user_in.login
    user.phone_number = user_in.phone_number
    user.address = user_in.address
    user.view_history = user_in.view_history
    user.purchase_history = user_in.purchase_history
    user.about_employee = user_in.about_employee
    user.hashed_password = hashed_password
    user.role = UserRole.ADMIN
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate) -> User | None:

    user = await db.get(User, user_id)
    if user is None:
        return None
    updates = user_in.model_dump(exclude_unset=True)
    for field_name, value in updates.items():
        setattr(user, field_name, value)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_role(db: AsyncSession, user: User, role: UserRole) -> User:

    user.role = role
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:

    user = await db.get(User, user_id)
    if user is None:
        return False
    await db.delete(user)
    await db.commit()
    return True
