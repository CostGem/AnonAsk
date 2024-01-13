from sqlalchemy import (
    ForeignKey,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class AchievementModel(BaseModel):
    __tablename__ = "achievements"

    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    award_status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)
