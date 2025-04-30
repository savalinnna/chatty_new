from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.deps import get_db, get_current_user
from schemas.comment import CommentCreate, CommentUpdate, CommentRead
from services.comment_service import CommentService

router = APIRouter(prefix="/comments", tags=["Comments"])
security_scheme = HTTPBearer()

@router.post("/", response_model=CommentRead, dependencies=[Depends(security_scheme)])
async def create_comment(
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return await CommentService.create_comment(db, comment_in, user_id)

@router.get("/", response_model=List[CommentRead])
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    return await CommentService.get_comments_for_post(db, post_id)

@router.patch("/{comment_id}", response_model=CommentRead, dependencies=[Depends(security_scheme)])
async def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return await CommentService.update_comment(db, comment_id, comment_update, user_id)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security_scheme)])
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    await CommentService.delete_comment(db, comment_id, user_id)
    return None
