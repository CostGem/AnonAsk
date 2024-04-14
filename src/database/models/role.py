from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class RoleModel(BaseModel):
    __tablename__ = "roles"

    emoji: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
