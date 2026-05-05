from __future__ import annotations
import os
from collections.abc import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import app.models  # noqa: F401
from app.api.deps import get_db
from app.core.config import settings
from app.core.security import hash_password
from app.db.base import Base
from app.main import app
from app.models.category import Category
from app.models.product import Product
from app.models.user import User, UserRole

settings.SECRET_KEY = "test-secret-key-with-at-least-32-bytes"
settings.ADMIN_BOOTSTRAP_ENABLED = False


def get_test_database_url() -> str:
    database_url = os.environ.get("TEST_DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "TEST_DATABASE_URL is not set. Run tests via "
            "'docker compose --profile test up --build tests'."
        )
    return database_url


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(get_test_database_url())
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
def client(db_session: AsyncSession) -> Generator[TestClient, None, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def created_user(db_session: AsyncSession) -> User:
    user = User(
        name="Test User",
        email="user@example.com",
        login="test-user",
        phone_number="+380501112233",
        hashed_password=hash_password("123456"),
        role=UserRole.USER,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession) -> User:
    user = User(
        name="Admin User",
        email="admin@example.com",
        login="admin-user",
        hashed_password=hash_password("123456"),
        role=UserRole.ADMIN,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def staff_user(db_session: AsyncSession) -> User:
    user = User(
        name="Staff User",
        email="staff@example.com",
        login="staff-user",
        hashed_password=hash_password("123456"),
        role=UserRole.STAFF,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def seeded_product(db_session: AsyncSession) -> Product:
    category = Category(name="Chinese")
    db_session.add(category)
    await db_session.flush()

    product = Product(
        name="Tie Guan Yin",
        native_name="铁观音",
        description="Test tea",
        image_filename="Sphagnum.jpg",
        kind="oolong",
        price_uah=320,
        stock_quantity=12,
        reviews="Nice tea",
        categories=[category],
    )
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)
    return product
