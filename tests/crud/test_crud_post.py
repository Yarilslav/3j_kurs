from __future__ import annotations

import pytest

from app.crud import crud_post
from app.schemas.post import PostCreate


@pytest.mark.asyncio
async def test_create_post_persists_post(db_session, created_user):
    post = await crud_post.create_post(
        db_session,
        created_user.id,
        PostCreate(title="Test post", content="CRUD content"),
    )

    assert post.id is not None
    assert post.user_id == created_user.id
    assert post.title == "Test post"
