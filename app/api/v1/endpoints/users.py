from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_admin_user, get_current_user
from app.core.security import hash_password
from app.crud import crud_user
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse, UserRoleUpdate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):

    return await crud_user.get_users(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):

    existing_email = await crud_user.get_user_by_email(db, user.email)
    if existing_email is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_login = await crud_user.get_user_by_login(db, user.login)
    if existing_login is not None:
        raise HTTPException(status_code=400, detail="Login already registered")
    hashed_password = hash_password(user.password)
    return await crud_user.create_user(db, user, hashed_password)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if user.email is not None:
        existing_email = await crud_user.get_user_by_email(db, user.email)
        if existing_email is not None and existing_email.id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")
    if user.login is not None:
        existing_login = await crud_user.get_user_by_login(db, user.login)
        if existing_login is not None and existing_login.id != user_id:
            raise HTTPException(status_code=400, detail="Login already registered")

    updated = await crud_user.update_user(db, user_id, user)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    deleted = await crud_user.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "deleted"}


@router.patch("/by-login/{login}/role", response_model=UserResponse)
async def update_user_role(
    login: str,
    payload: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    user = await crud_user.get_user_by_login(db, login)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud_user.update_user_role(db, user, payload.role)
