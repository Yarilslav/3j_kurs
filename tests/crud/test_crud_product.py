from __future__ import annotations

import pytest

from app.crud import crud_product


@pytest.mark.asyncio
async def test_get_products_returns_seeded_product(db_session, seeded_product):
    products = await crud_product.get_products(db_session)

    assert len(products) == 1
    assert products[0].id == seeded_product.id
