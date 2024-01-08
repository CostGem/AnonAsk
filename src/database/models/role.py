from sqlalchemy import (
    BigInteger,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import BaseModel


class RoleModel(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String, nullable=True)
    level: Mapped[int] = mapped_column(BigInteger, nullable=False)
