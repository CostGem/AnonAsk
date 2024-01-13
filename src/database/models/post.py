from sqlalchemy import (
    BigInteger,
    Boolean
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class PostModel(BaseModel):
    __tablename__ = "posts"

    post_id_in_chat: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_commentable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
