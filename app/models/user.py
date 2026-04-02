"""User model for PostgreSQL."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.profile import Profile


class User(Base):
    """Users table."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # One-to-many: one user -> many posts.
    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    # One-to-one: one user -> one profile.
    profile: Mapped[Optional["Profile"]] = relationship(back_populates="user", uselist=False)
