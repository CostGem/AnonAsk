import datetime

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Date
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class ScheduleModel(BaseModel):
    __tablename__ = "schedules"

    
    media_id: Mapped[int] = mapped_column(
        ForeignKey("media.id", ondelete="cascade"),
        nullable=False
    )
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    added_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    added_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
