from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_staff_or_admin_user
from app.crud import crud_product
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):

    products = await crud_product.get_products(db)
    return [ProductResponse.from_product(product) for product in products]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):

    product = await crud_product.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.from_product(product)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _staff=Depends(get_staff_or_admin_user),
):

    created = await crud_product.create_product(db, product)
    return ProductResponse.from_product(created)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    _staff=Depends(get_staff_or_admin_user),
):
    product = await crud_product.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = await crud_product.update_product(db, product, product_in)
    return ProductResponse.from_product(updated)


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    _staff=Depends(get_staff_or_admin_user),
):
    product = await crud_product.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await crud_product.delete_product(db, product)
    return {"message": "deleted"}
