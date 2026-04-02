"""add moss models

Revision ID: e8fd94fd3d4d
Revises: ff332bc3a388
Create Date: 2026-03-15 15:11:47.675683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8fd94fd3d4d'
down_revision: Union[str, Sequence[str], None] = 'ff332bc3a388'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("bio", sa.Text, nullable=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, unique=True),
    )
    op.create_index("ix_profiles_id", "profiles", ["id"])

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )
    op.create_index("ix_posts_id", "posts", ["id"])
    op.create_index("ix_posts_user_id", "posts", ["user_id"])

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
    )
    op.create_index("ix_categories_id", "categories", ["id"])

    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("steepness_index", sa.Float, nullable=False),
        sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id"), nullable=False),
    )
    op.create_index("ix_products_id", "products", ["id"])
    op.create_index("ix_products_category_id", "products", ["category_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_products_category_id", table_name="products")
    op.drop_index("ix_products_id", table_name="products")
    op.drop_table("products")

    op.drop_index("ix_categories_id", table_name="categories")
    op.drop_table("categories")

    op.drop_index("ix_posts_user_id", table_name="posts")
    op.drop_index("ix_posts_id", table_name="posts")
    op.drop_table("posts")

    op.drop_index("ix_profiles_id", table_name="profiles")
    op.drop_table("profiles")
