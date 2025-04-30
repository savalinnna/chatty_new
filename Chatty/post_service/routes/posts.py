from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.deps import get_db, get_current_user
from schemas.post import PostCreate, PostUpdate, PostRead
from services.post_service import PostService
from storage.image_uploader import upload_image_to_s3

router = APIRouter(prefix="/posts", tags=["Posts"])
security_scheme = HTTPBearer()

@router.post("/", response_model=PostRead, dependencies=[Depends(security_scheme)])
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    image_url = await upload_image_to_s3(file) if file else None
    post_data = PostCreate(title=title, content=content, image_url=image_url)
    return await PostService.create_post(db, post_data, user_id)

@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    return await PostService.get_post(db, post_id)

@router.patch("/{post_id}", response_model=PostRead, dependencies=[Depends(security_scheme)])
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return await PostService.update_post(db, post_id, post_update, user_id)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security_scheme)])
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    await PostService.delete_post(db, post_id, user_id)
    return None
