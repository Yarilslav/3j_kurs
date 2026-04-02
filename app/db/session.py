"""Database session setup using SQLAlchemy AsyncSession."""

from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# Async SQLAlchemy engine for PostgreSQL.
engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Async session factory for DB access.
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide an async database session for a request lifecycle."""

    async with AsyncSessionLocal() as session:
        yield session
