from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Index,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel
from src.utils.service.time import utcnow


class UserModel(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    is_chat_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    register_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    __table_args__ = (Index("users_user_id_idx", user_id, unique=True),)
