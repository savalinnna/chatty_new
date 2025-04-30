from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from models import Comment
from schemas.comment import CommentCreate, CommentUpdate

class CommentService:
    @staticmethod
    async def create_comment(db: AsyncSession, comment_in: CommentCreate, user_id: int):
        comment = Comment(**comment_in.dict(), user_id=user_id)
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def get_comments_for_post(db: AsyncSession, post_id: int):
        result = await db.execute(select(Comment).where(Comment.post_id == post_id))
        return result.scalars().all()

    @staticmethod
    async def update_comment(db: AsyncSession, comment_id: int, comment_in: CommentUpdate, user_id: int):
        comment = await db.get(Comment, comment_id)
        if not comment or comment.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        comment.content = comment_in.content
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def delete_comment(db: AsyncSession, comment_id: int, user_id: int):
        comment = await db.get(Comment, comment_id)
        if not comment or comment.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        await db.delete(comment)
        await db.commit()
