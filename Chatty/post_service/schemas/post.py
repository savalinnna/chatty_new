from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostRead(PostCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
