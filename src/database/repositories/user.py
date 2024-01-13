from typing import Optional, List

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import UserModel, StatusModel, UserStatusModel
from src.database.repositories import StatusRepository
from src.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    """User repository"""

    def __init__(self, session: AsyncSession):
        """Initialize user repository"""

        super().__init__(session=session)

    async def register(self, user_id: int, name: str, username: Optional[str] = None) -> UserModel:
        """
        Register new user if not exists

        :param user_id: User ID
        :param name: Name of the user
        :param username: Username of the user
        """

        if user := await self.get(user_id=user_id):
            if user.username != username or user.name != name:
                await self.session.execute(
                    update(
                        table=UserModel
                    ).where(
                        UserModel.id == user.id
                    ).values(
                        username=username,
                        name=name
                    )
                )
        else:
            self.session.add(
                instance=UserModel(
                    user_id=user_id,
                    name=name,
                    username=username,
                    role_id=1,
                    status_id=1
                )
            )

            user = await self.get(user_id=user_id)

            await StatusRepository(session=self.session).give_default_statuses_to_user(user_id=user.id)

            return user

    async def get(self, user_id: int) -> Optional[UserModel]:
        """
        Return user by ID

        :param user_id: User ID
        """

        return await self.session.scalar(
            select(UserModel).where(UserModel.user_id == user_id)
        )

    async def get_status(self, user: UserModel) -> StatusModel:
        """
        Return user status

        :param user: User object
        """

        user_status = await self.session.scalar(
            select(UserStatusModel.status_id).where(UserModel.user_id == user.id)
        )

        return await self.session.scalar(
            select(StatusModel).where(StatusModel.id == user_status)
        )

    async def nickname_is_taken(self, nickname: str) -> bool:
        """
        Return True if nickname is taken, else False

        :param nickname: Nickname
        """

        exist_user = await self.session.scalar(
            select(UserModel.nickname).where(UserModel.nickname.ilike(f"%{nickname}%"))
        )

        return exist_user is not None

    async def get_not_bot_blocked_users_count(self) -> int:
        """Returns the number of users who have not blocked the bot"""

        return await self.session.scalar(
            select(func.count(UserModel.user_id)).where(UserModel.is_chat_blocked == False)
        )

    async def get_not_bot_blocked_users(self) -> List[UserModel]:
        """Returns all users who have not blocked the bot"""

        users = await self.session.scalars(
            select(UserModel.user_id).where(UserModel.is_chat_blocked == False)
        )

        return users.all()
