"""rebuild products and add orders reservations

Revision ID: a1c4f6e8b9d2
Revises: f0a8d3c1b2e4
Create Date: 2026-05-05 00:00:00.000000

"""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "a1c4f6e8b9d2"
down_revision: Union[str, Sequence[str], None] = "f0a8d3c1b2e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


order_status_enum = postgresql.ENUM("pending", "confirmed", "completed", "cancelled", name="order_status")
reservation_status_enum = postgresql.ENUM("pending", "confirmed", "completed", "cancelled", name="reservation_status")
order_status_column_enum = postgresql.ENUM(
    "pending",
    "confirmed",
    "completed",
    "cancelled",
    name="order_status",
    create_type=False,
)
reservation_status_column_enum = postgresql.ENUM(
    "pending",
    "confirmed",
    "completed",
    "cancelled",
    name="reservation_status",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    order_status_enum.create(bind, checkfirst=True)
    reservation_status_enum.create(bind, checkfirst=True)

    op.add_column("products", sa.Column("native_name", sa.String(length=255), nullable=True))
    op.add_column("products", sa.Column("image_filename", sa.String(length=255), nullable=True))
    op.add_column("products", sa.Column("kind", sa.String(length=255), nullable=True))
    op.add_column("products", sa.Column("price_uah", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("products", sa.Column("stock_quantity", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("products", sa.Column("reviews", sa.Text(), nullable=True))

    op.create_table(
        "product_categories",
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id", ondelete="CASCADE"), nullable=False),
        sa.PrimaryKeyConstraint("product_id", "category_id"),
    )

    rows = bind.execute(sa.text("SELECT id, category_id, image_path FROM products")).fetchall()
    for row in rows:
        if row.category_id is not None:
            bind.execute(
                sa.text(
                    "INSERT INTO product_categories (product_id, category_id) VALUES (:product_id, :category_id)"
                ),
                {"product_id": row.id, "category_id": row.category_id},
            )
        image_filename = None
        if row.image_path:
            image_filename = PurePosixPath(row.image_path).name
        bind.execute(
            sa.text(
                """
                UPDATE products
                SET kind = :kind,
                    image_filename = :image_filename
                WHERE id = :product_id
                """
            ),
            {
                "kind": "tea",
                "image_filename": image_filename,
                "product_id": row.id,
            },
        )

    op.alter_column("products", "kind", nullable=False)
    op.drop_index("ix_products_category_id", table_name="products")
    op.drop_column("products", "category_id")
    op.drop_column("products", "steepness_index")
    op.drop_column("products", "image_path")

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("guest_name", sa.String(length=255), nullable=True),
        sa.Column("guest_contact", sa.String(length=255), nullable=True),
        sa.Column("status", order_status_column_enum, nullable=False, server_default="pending"),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("total_price", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("what_ordered", sa.Text(), nullable=False),
    )
    op.create_index("ix_orders_id", "orders", ["id"])
    op.create_index("ix_orders_user_id", "orders", ["user_id"])

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Integer(), nullable=False),
        sa.Column("line_total", sa.Integer(), nullable=False),
    )
    op.create_index("ix_order_items_id", "order_items", ["id"])
    op.create_index("ix_order_items_order_id", "order_items", ["order_id"])
    op.create_index("ix_order_items_product_id", "order_items", ["product_id"])

    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("guest_name", sa.String(length=255), nullable=True),
        sa.Column("guest_contact", sa.String(length=255), nullable=True),
        sa.Column("reservation_at", sa.String(length=255), nullable=False),
        sa.Column("places", sa.String(length=255), nullable=False),
        sa.Column("status", reservation_status_column_enum, nullable=False, server_default="pending"),
        sa.Column("price", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_reservations_id", "reservations", ["id"])
    op.create_index("ix_reservations_user_id", "reservations", ["user_id"])


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_index("ix_reservations_user_id", table_name="reservations")
    op.drop_index("ix_reservations_id", table_name="reservations")
    op.drop_table("reservations")

    op.drop_index("ix_order_items_product_id", table_name="order_items")
    op.drop_index("ix_order_items_order_id", table_name="order_items")
    op.drop_index("ix_order_items_id", table_name="order_items")
    op.drop_table("order_items")

    op.drop_index("ix_orders_user_id", table_name="orders")
    op.drop_index("ix_orders_id", table_name="orders")
    op.drop_table("orders")

    op.add_column("products", sa.Column("image_path", sa.String(length=512), nullable=True))
    op.add_column("products", sa.Column("steepness_index", sa.Float(), nullable=False, server_default="0"))
    op.add_column("products", sa.Column("category_id", sa.Integer(), nullable=True))
    op.create_foreign_key("products_category_id_fkey", "products", "categories", ["category_id"], ["id"])
    op.create_index("ix_products_category_id", "products", ["category_id"])

    rows = bind.execute(sa.text("SELECT product_id, category_id FROM product_categories")).fetchall()
    for row in rows:
        bind.execute(
            sa.text("UPDATE products SET category_id = :category_id WHERE id = :product_id"),
            {"category_id": row.category_id, "product_id": row.product_id},
        )
    bind.execute(sa.text("UPDATE products SET steepness_index = 0 WHERE steepness_index IS NULL"))

    op.drop_table("product_categories")
    op.drop_column("products", "reviews")
    op.drop_column("products", "stock_quantity")
    op.drop_column("products", "price_uah")
    op.drop_column("products", "kind")
    op.drop_column("products", "image_filename")
    op.drop_column("products", "native_name")
    op.alter_column("products", "category_id", nullable=False)

    reservation_status_enum.drop(bind, checkfirst=True)
    order_status_enum.drop(bind, checkfirst=True)
