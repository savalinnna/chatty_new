from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from db.base import Base

class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column()

    post: Mapped["Post"] = relationship(back_populates="likes")