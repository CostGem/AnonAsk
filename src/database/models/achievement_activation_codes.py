from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import BaseModel


class AchievementActivationCodeModel(BaseModel):
    __tablename__ = "achievement_activation_codes"

    code: Mapped[str] = mapped_column(String, nullable=False)
    activations_limit: Mapped[int] = mapped_column(BigInteger, nullable=False)
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievements.id"), nullable=False)
    from_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    until_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
