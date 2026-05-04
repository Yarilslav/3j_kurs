from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.crud import crud_user
from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserRegistration, UserResponse

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegistration, db: AsyncSession = Depends(get_db)):

    existing_email = await crud_user.get_user_by_email(db, user.email)
    if existing_email is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_login = await crud_user.get_user_by_login(db, user.login)
    if existing_login is not None:
        raise HTTPException(status_code=400, detail="Login already registered")
    hashed_password = hash_password(user.password)
    return await crud_user.create_user(db, UserCreate(**user.model_dump()), hashed_password)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):

    user = await crud_user.get_user_by_login(db, payload.login)
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "login": user.login, "role": user.role.value})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
    )
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def me(current_user=Depends(get_current_user)):

    return current_user
