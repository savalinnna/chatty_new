from pydantic import BaseModel

class CommentCreate(BaseModel):
    post_id: int
    content: str

class CommentUpdate(BaseModel):
    content: str

class CommentRead(CommentCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
