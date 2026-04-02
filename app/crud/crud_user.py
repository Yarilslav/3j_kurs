"""User CRUD operations using SQLAlchemy AsyncSession."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_users(db: AsyncSession) -> list[User]:
    """Return all users."""

    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Return a user by email."""

    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Return a user by ID."""

    return await db.get(User, user_id)


async def get_user_by_name(db: AsyncSession, name: str) -> User | None:
    """Return a user by name."""

    result = await db.execute(select(User).where(User.name == name))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_in: UserCreate, hashed_password: str) -> User:
    """Create a new user."""

    user = User(name=user_in.name, email=user_in.email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate) -> User | None:
    """Update an existing user by ID."""

    user = await db.get(User, user_id)
    if user is None:
        return None
    user.name = user_in.name
    user.email = user_in.email
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """Delete a user by ID."""

    user = await db.get(User, user_id)
    if user is None:
        return False
    await db.delete(user)
    await db.commit()
    return True
