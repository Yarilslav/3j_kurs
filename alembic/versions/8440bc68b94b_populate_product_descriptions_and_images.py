"""populate product descriptions and images

Revision ID: 8440bc68b94b
Revises: 61e50e1f617a
Create Date: 2026-03-15 16:03:37.665110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8440bc68b94b'
down_revision: Union[str, Sequence[str], None] = '61e50e1f617a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "UPDATE products SET description = 'Класичний болотний мох, добре утримує вологу, підходить для флораріумів.', "
        "image_path = 'assets/moss_images/Sphagnum.jpg' WHERE id = 1"
    )
    op.execute(
        "UPDATE products SET description = 'Лісовий мох з високими стеблами, гарний для грунтового покриття.', "
        "image_path = 'assets/moss_images/Polytrichum.jpeg' WHERE id = 2"
    )
    op.execute(
        "UPDATE products SET description = 'М''який лісовий мох, часто використовують для декоративних композицій.', "
        "image_path = 'assets/moss_images/Hypnum.jpg' WHERE id = 3"
    )
    op.execute(
        "UPDATE products SET description = 'Декоративний мох, схожий на зелені подушки, ідеальний для міні-садів.', "
        "image_path = 'assets/moss_images/Leucobryum.jpg' WHERE id = 4"
    )
    op.execute(
        "UPDATE products SET description = 'Компактний лісовий мох, невибагливий до світла і вологи.', "
        "image_path = 'assets/moss_images/Bryum.jpg' WHERE id = 5"
    )
    op.execute(
        "UPDATE products SET description = 'Ще один лісовий мох з густими пучками, підходить для тераріумів.', "
        "image_path = 'assets/moss_images/Dicranum.jpg' WHERE id = 6"
    )
    op.execute(
        "UPDATE products SET description = 'Болотний мох, любить воду, гарний для акваріумів або вологих флораріумів.', "
        "image_path = 'assets/moss_images/Fontinalis.jpg' WHERE id = 7"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "UPDATE products SET description = NULL, image_path = NULL WHERE id BETWEEN 1 AND 7"
    )
