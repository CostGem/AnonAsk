from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import UserModel
from src.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    """User repository"""

    def __init__(self, session: AsyncSession):
        """Initialize user repository"""

        super().__init__(session=session)

    async def register(self, user_id: int, name: str, username: Optional[str] = None) -> UserModel:
        """Register new user if not exists"""

        pass

    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """
        Returns a user by user ID

        :param user_id: User ID
        """

        return await self.session.scalar(
            select(UserModel).where(UserModel.user_id == user_id)
        )

    async def get_by_pk(self, user_id: int) -> Optional[UserModel]:
        """
        Returns a user by pk

        :param user_id: User pk
        """

        return await self.session.scalar(
            select(UserModel).where(UserModel.id == user_id)
        )

    async def update_chat_blocked(self, user: UserModel, chat_blocked: bool) -> None:
        """
        Update is_chat_blocked status for user

        :param user: User
        :param chat_blocked: Chat blocked status
        """

        await self.session.execute(
            update(
                table=UserModel
            ).where(
                UserModel.id == user.id
            ).values(
                is_chat_blocked=chat_blocked
            )
        )

        await self.session.commit()
