from datetime import time

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Time
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import BaseModel


class LessonModel(BaseModel):
    __tablename__ = "lessons"

    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedule_types.id"), nullable=False)
    number: Mapped[int] = mapped_column(BigInteger, nullable=False)
    start_at: Mapped[time] = mapped_column(Time, nullable=False)
    end_at: Mapped[time] = mapped_column(Time, nullable=False)
