from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from models.post import Post
from schemas.post import PostCreate, PostUpdate

class PostService:
    @staticmethod
    async def create_post(db: AsyncSession, post_in: PostCreate, user_id: int):
        post = Post(**post_in.dict(), user_id=user_id)
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def get_post(db: AsyncSession, post_id: int):
        post = await db.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    @staticmethod
    async def update_post(db: AsyncSession, post_id: int, post_in: PostUpdate, user_id: int):
        post = await db.get(Post, post_id)
        if not post or post.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        for field, value in post_in.dict(exclude_unset=True).items():
            setattr(post, field, value)
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def delete_post(db: AsyncSession, post_id: int, user_id: int):
        post = await db.get(Post, post_id)
        if not post or post.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        await db.delete(post)
        await db.commit()
