"""SQLAlchemy Base for declarative models."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base class for all models."""


# Model imports are handled in app.models for Alembic autogenerate.
