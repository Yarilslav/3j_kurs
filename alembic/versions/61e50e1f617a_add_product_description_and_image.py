"""add product description and image

Revision ID: 61e50e1f617a
Revises: 2ddb3a7b5f4c
Create Date: 2026-03-15 16:01:02.928215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61e50e1f617a'
down_revision: Union[str, Sequence[str], None] = '2ddb3a7b5f4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("products", sa.Column("description", sa.Text, nullable=True))
    op.add_column("products", sa.Column("image_path", sa.String(length=512), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("products", "image_path")
    op.drop_column("products", "description")
