from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.security import hash_password
from app.crud import crud_user
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):

    return await crud_user.get_users(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):

    hashed_password = hash_password(user.password)
    return await crud_user.create_user(db, user, hashed_password)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):

    updated = await crud_user.update_user(db, user_id, user)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user=Depends(get_current_user),
):

    if _current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    deleted = await crud_user.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "deleted"}
