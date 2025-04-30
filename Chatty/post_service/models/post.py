from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, func
from db.base import Base
from typing import List
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    comments: Mapped[List["Comment"]] = relationship(back_populates="post", cascade="all, delete")
    likes: Mapped[List["Like"]] = relationship(back_populates="post", cascade="all, delete")

