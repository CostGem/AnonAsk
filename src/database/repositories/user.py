"""User repository file."""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import UserModel
from src.database.repositories.abstract import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    """User repository"""

    def __init__(self, session: AsyncSession):
        """Initialize user repository"""

        super().__init__(session=session)

    async def create(self) -> None:
        await self.session.merge(UserModel())

    async def get(self, user_id: int) -> Optional[UserModel]:
        return await self.session.scalar(
            select(UserModel).where(UserModel.user_id == user_id)
        )
