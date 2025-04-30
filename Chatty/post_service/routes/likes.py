from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, get_current_user
from schemas.like import LikeCreate
from services.like_service import LikeService

router = APIRouter(prefix="/likes", tags=["Likes"])
security_scheme = HTTPBearer()

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(security_scheme)])
async def like_post(
    like_in: LikeCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    await LikeService.like_post(db, like_in.post_id, user_id)
    return {"detail": "Liked"}

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security_scheme)])
async def unlike_post(
    like_in: LikeCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    await LikeService.unlike_post(db, like_in.post_id, user_id)
    return None
