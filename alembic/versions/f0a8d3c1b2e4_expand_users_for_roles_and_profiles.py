"""expand users for roles and profiles

Revision ID: f0a8d3c1b2e4
Revises: 9c2f8f6a3b1d
Create Date: 2026-05-04 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f0a8d3c1b2e4"
down_revision: Union[str, Sequence[str], None] = "9c2f8f6a3b1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


role_enum = sa.Enum("user", "staff", "admin", name="user_role")


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    role_enum.create(bind, checkfirst=True)

    op.add_column("users", sa.Column("login", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("phone_number", sa.String(length=20), nullable=True))
    op.add_column(
        "users",
        sa.Column("role", role_enum, nullable=False, server_default="user"),
    )
    op.add_column("users", sa.Column("address", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("view_history", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("purchase_history", sa.Text(), nullable=True))
    op.add_column(
        "users",
        sa.Column("bonus_points", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column("users", sa.Column("about_employee", sa.Text(), nullable=True))

    op.execute("UPDATE users SET login = 'user_' || id WHERE login IS NULL")

    op.alter_column("users", "login", nullable=False)
    op.create_index(op.f("ix_users_login"), "users", ["login"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()

    op.drop_index(op.f("ix_users_login"), table_name="users")
    op.drop_column("users", "about_employee")
    op.drop_column("users", "bonus_points")
    op.drop_column("users", "purchase_history")
    op.drop_column("users", "view_history")
    op.drop_column("users", "address")
    op.drop_column("users", "role")
    op.drop_column("users", "phone_number")
    op.drop_column("users", "login")

    role_enum.drop(bind, checkfirst=True)
