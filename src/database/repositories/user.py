"""User repository file."""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import UserModel
from src.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=UserModel, session=session)

    async def new(self) -> None:
        await self.session.merge(UserModel())
