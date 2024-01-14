import datetime

from sqlalchemy import (
    BigInteger,
    ForeignKey, DateTime
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class CommentModel(BaseModel):
    __tablename__ = "comments"

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    parent_comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), nullable=True)
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    commented_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=False)
