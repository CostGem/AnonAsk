from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Index,
    String,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel
from src.enums.role import Role


class UserModel(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
        default=Role.USER
    )

    is_chat_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    register_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (Index("users_user_id_idx", user_id, unique=True),)
