from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    DateTime, func
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import BaseModel


class UserStatusModel(BaseModel):
    __tablename__ = "user_statuses"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now)
