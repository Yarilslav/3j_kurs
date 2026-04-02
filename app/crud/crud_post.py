"""Post CRUD operations."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate


async def create_post(db: AsyncSession, user_id: int, post_in: PostCreate) -> Post:
    """Create a new post."""

    post = Post(title=post_in.title, content=post_in.content, user_id=user_id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post
