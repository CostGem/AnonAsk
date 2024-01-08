from sqlalchemy import (
    BigInteger,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import BaseModel


class ScheduleTypeModel(BaseModel):
    __tablename__ = "schedule_types"

    name: Mapped[str] = mapped_column(String, nullable=True)
