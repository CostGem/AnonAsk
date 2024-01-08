from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import BaseModel


class UserAchievementActivationModel(BaseModel):
    __tablename__ = "users_achievement_activations"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    activation_code_id: Mapped[int] = mapped_column(ForeignKey("achievement_activation_codes.id"), nullable=False)
    activated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now, nullable=False)
