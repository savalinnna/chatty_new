from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.like import Like

class LikeService:
    @staticmethod
    async def like_post(db: AsyncSession, post_id: int, user_id: int):
        result = await db.execute(
            select(Like).where(Like.post_id == post_id, Like.user_id == user_id)
        )
        like = result.scalar_one_or_none()
        if not like:
            like = Like(post_id=post_id, user_id=user_id)
            db.add(like)
            await db.commit()

    @staticmethod
    async def unlike_post(db: AsyncSession, post_id: int, user_id: int):
        await db.execute(
            delete(Like).where(Like.post_id == post_id, Like.user_id == user_id)
        )
        await db.commit()
