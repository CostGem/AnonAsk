import datetime

from sqlalchemy import (
    Date,
    ForeignKey,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class TimetableModel(BaseModel):
    __tablename__ = "timetables"

    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedule_types.id"), nullable=False)
    photo: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
