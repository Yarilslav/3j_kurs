"""add users hashed password

Revision ID: 9c2f8f6a3b1d
Revises: 8440bc68b94b
Create Date: 2026-03-26 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9c2f8f6a3b1d"
down_revision: Union[str, Sequence[str], None] = "8440bc68b94b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("hashed_password", sa.String(length=255), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "hashed_password")
