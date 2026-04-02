from __future__ import annotations
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Profile(Base):

    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)

    user: Mapped["User"] = relationship(back_populates="profile")
