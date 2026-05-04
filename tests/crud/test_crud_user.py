from __future__ import annotations

import pytest

from app.core.bootstrap import ensure_root_admin
from app.core.config import settings
from app.crud import crud_user
from app.models.user import UserRole
from app.schemas.user import UserCreate, UserUpdate


@pytest.mark.asyncio
async def test_create_and_read_user(db_session):
    created = await crud_user.create_user(
        db_session,
        UserCreate(
            name="Test",
            email="Tester@example.com",
            login="tester-login",
            phone_number="+380501234567",
            password="123456",
        ),
        "hashed-password",
    )

    by_id = await crud_user.get_user_by_id(db_session, created.id)
    by_email = await crud_user.get_user_by_email(db_session, created.email)
    by_login = await crud_user.get_user_by_login(db_session, created.login)
    all_users = await crud_user.get_users(db_session)

    assert by_id is not None
    assert by_email is not None
    assert by_login is not None
    assert len(all_users) == 1
    assert by_email.id == created.id
    assert by_login.id == created.id


@pytest.mark.asyncio
async def test_update_user_updates_fields(db_session, created_user):
    updated = await crud_user.update_user(
        db_session,
        created_user.id,
        UserUpdate(name="Updated", email="updated@example.com", login="updated-login"),
    )

    assert updated is not None
    assert updated.name == "Updated"
    assert updated.email == "updated@example.com"
    assert updated.login == "updated-login"


@pytest.mark.asyncio
async def test_update_user_returns_none_for_missing_record(db_session):
    updated = await crud_user.update_user(
        db_session,
        999,
        UserUpdate(name="Missing", email="missing@example.com"),
    )

    assert updated is None


@pytest.mark.asyncio
async def test_delete_user_removes_record(db_session, created_user):
    deleted = await crud_user.delete_user(db_session, created_user.id)
    found = await crud_user.get_user_by_id(db_session, created_user.id)

    assert deleted is True
    assert found is None


@pytest.mark.asyncio
async def test_delete_user_returns_false_for_missing_record(db_session):
    deleted = await crud_user.delete_user(db_session, 999)

    assert deleted is False


@pytest.mark.asyncio
async def test_ensure_root_admin_creates_expected_admin(db_session):
    settings.ADMIN_BOOTSTRAP_ENABLED = True

    await ensure_root_admin(db_session)

    admin = await crud_user.get_user_by_login(db_session, settings.ADMIN_LOGIN)
    assert admin is not None
    assert admin.name == "Asahi Admin"
    assert admin.email == "yarilslaven@gmail.com"
    assert admin.role == UserRole.ADMIN
    assert admin.phone_number is None
    assert admin.address is None
    assert admin.view_history is None
    assert admin.purchase_history is None
    assert admin.about_employee is None


@pytest.mark.asyncio
async def test_ensure_root_admin_upgrades_existing_account(db_session):
    settings.ADMIN_BOOTSTRAP_ENABLED = True
    existing_user = await crud_user.create_user(
        db_session,
        UserCreate(
            name="Regular User",
            email="yarilslaven@gmail.com",
            login="other-login",
            password="123456",
            purchase_history="old history",
        ),
        "old-hash",
    )

    await ensure_root_admin(db_session)

    admin = await crud_user.get_user_by_id(db_session, existing_user.id)
    assert admin is not None
    assert admin.login == "string"
    assert admin.role == UserRole.ADMIN
    assert admin.purchase_history is None
