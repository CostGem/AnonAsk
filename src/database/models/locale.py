from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class LocaleModel(BaseModel):
    __tablename__ = "locales"

    emoji: Mapped[str] = mapped_column(String(5), nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    code: Mapped[str] = mapped_column(String(10), nullable=False)
