from __future__ import annotations

import pytest

from app.crud import crud_user
from app.schemas.user import UserCreate, UserUpdate


@pytest.mark.asyncio
async def test_create_and_read_user(db_session):
    created = await crud_user.create_user(
        db_session,
        UserCreate(name="Test", email="Tester@example.com", password="123456"),
        "hashed-password",
    )

    by_id = await crud_user.get_user_by_id(db_session, created.id)
    by_email = await crud_user.get_user_by_email(db_session, created.email)
    by_name = await crud_user.get_user_by_name(db_session, created.name)
    all_users = await crud_user.get_users(db_session)

    assert by_id is not None
    assert by_email is not None
    assert by_name is not None
    assert len(all_users) == 1
    assert by_email.id == created.id
    assert by_name.id == created.id


@pytest.mark.asyncio
async def test_update_user_updates_fields(db_session, created_user):
    updated = await crud_user.update_user(
        db_session,
        created_user.id,
        UserUpdate(name="Updated", email="updated@example.com"),
    )

    assert updated is not None
    assert updated.name == "Updated"
    assert updated.email == "updated@example.com"


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
