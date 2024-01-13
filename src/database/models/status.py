from sqlalchemy import (
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class StatusModel(BaseModel):
    __tablename__ = "statuses"

    emoji: Mapped[str] = mapped_column(String(5), nullable=True)
