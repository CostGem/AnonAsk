import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Index,
    String,
    ForeignKey, func
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), nullable=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)
    locale_id: Mapped[int] = mapped_column(ForeignKey("locales.id"), nullable=False)

    is_chat_blocked: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    register_date: Mapped[str] = mapped_column(
        DateTime, server_default=func.now, nullable=False
    )

    __table_args__ = (Index("users_user_id_idx", user_id, unique=True),)
