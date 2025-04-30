from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Subscription
from typing import List
from fastapi import HTTPException, status
import httpx
from app.core.config import settings

async def get_user_id_by_username(username: str) -> int:
    """Fetch user ID from username via Auth Service."""
    try:
        url = f"{settings.url_auth_service}/auth/internal/user-id-by-username"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"username": username})
        if response.status_code == 200:
            return response.json()["user_id"]
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(status_code=500, detail="Auth service error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user ID: {str(e)}")

async def get_following(user_id: int, db: AsyncSession) -> List[int]:
    """Get list of user IDs that the given user follows."""
    result = await db.execute(
        select(Subscription.user_id).where(Subscription.follower_id == user_id)
    )
    return result.scalars().all()

async def get_followers_ids(user_id: int, db: AsyncSession) -> List[int]:
    """Get list of user IDs that follow the given user."""
    result = await db.execute(
        select(Subscription.follower_id).where(Subscription.user_id == user_id)
    )
    return result.scalars().all()