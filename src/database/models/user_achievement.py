from sqlalchemy import (
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class UserAchievementModel(BaseModel):
    __tablename__ = "user_achievements"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievements.id"), nullable=False)
