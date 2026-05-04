from __future__ import annotations

from enum import StrEnum
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.profile import Profile


class UserRole(StrEnum):
    USER = "user"
    STAFF = "staff"
    ADMIN = "admin"


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    login: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            values_callable=lambda enum_cls: [role.value for role in enum_cls],
        ),
        nullable=False,
        default=UserRole.USER,
        server_default=UserRole.USER.value,
    )
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    view_history: Mapped[str | None] = mapped_column(Text, nullable=True)
    purchase_history: Mapped[str | None] = mapped_column(Text, nullable=True)
    bonus_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    about_employee: Mapped[str | None] = mapped_column(Text, nullable=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    profile: Mapped[Optional["Profile"]] = relationship(back_populates="user", uselist=False)
