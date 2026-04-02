from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.crud import crud_post
from app.db.session import get_db
from app.schemas.post import PostCreate, PostResponse

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return await crud_post.create_post(db, current_user.id, post)
