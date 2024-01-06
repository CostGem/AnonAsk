import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Index,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class UsersTable(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    locale: Mapped[str] = mapped_column(String, nullable=False)
    is_chat_blocked: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    register_date: Mapped[str] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )

    __table_args__ = (Index("users_user_id_idx", user_id, unique=True),)
