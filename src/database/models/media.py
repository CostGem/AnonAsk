from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import BaseModel


class MediaModel(BaseModel):
    __tablename__ = "media"

    file_type: Mapped[str] = mapped_column(String, nullable=False)
    file_id: Mapped[str] = mapped_column(String, nullable=False)
