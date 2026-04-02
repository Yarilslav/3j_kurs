"""seed moss categories and products

Revision ID: 2ddb3a7b5f4c
Revises: e8fd94fd3d4d
Create Date: 2026-03-15 15:57:09.345637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ddb3a7b5f4c'
down_revision: Union[str, Sequence[str], None] = 'e8fd94fd3d4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    category_table = sa.table(
        "categories",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )

    product_table = sa.table(
        "products",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("steepness_index", sa.Float),
        sa.column("category_id", sa.Integer),
    )

    op.bulk_insert(
        category_table,
        [
            {"id": 1, "name": "Болотний"},
            {"id": 2, "name": "Лісовий"},
            {"id": 3, "name": "Декоративний"},
        ],
    )

    op.bulk_insert(
        product_table,
        [
            {
                "id": 1,
                "name": "Sphagnum",
                "steepness_index": 8,
                "category_id": 1,
            },
            {
                "id": 2,
                "name": "Polytrichum",
                "steepness_index": 6,
                "category_id": 2,
            },
            {
                "id": 3,
                "name": "Hypnum",
                "steepness_index": 5,
                "category_id": 2,
            },
            {
                "id": 4,
                "name": "Leucobryum",
                "steepness_index": 7,
                "category_id": 3,
            },
            {
                "id": 5,
                "name": "Bryum",
                "steepness_index": 4,
                "category_id": 2,
            },
            {
                "id": 6,
                "name": "Dicranum",
                "steepness_index": 6,
                "category_id": 2,
            },
            {
                "id": 7,
                "name": "Fontinalis",
                "steepness_index": 7,
                "category_id": 1,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM products WHERE id BETWEEN 1 AND 7")
    op.execute("DELETE FROM categories WHERE id BETWEEN 1 AND 3")
