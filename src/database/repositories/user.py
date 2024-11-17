from typing import Optional

from sqlalchemy import select, update

from src.database.models import UserModel
from src.database.repositories.abstract import AbstractRepository


class UserRepository(AbstractRepository[UserModel]):
    """User repository"""

    type_model = UserModel

    async def register(self, user_id: int, name: str, username: Optional[str] = None) -> UserModel:
        """
        Register new user if not exists

        :param user_id: User ID
        :param name: User name
        :param username: Username
        """

        if user := await self.get_by_id(user_id=user_id):
            await self.session.execute(
                update(UserModel)
                .where(UserModel.id == user.id)
                .values(
                    name=name,
                    username=username
                )
            )
        else:
            user: UserModel = UserModel(
                user_id=user_id,
                name=name,
                username=username
            )

            self.session.add(instance=user)

        await self.session.commit()

        return user

    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """
        Returns a user by user ID

        :param user_id: User ID
        """

        return await self.session.scalar(
            select(UserModel)
            .where(UserModel.user_id == user_id)
        )

    async def set_chat_blocked(self, user: UserModel, chat_blocked: bool) -> None:
        """
        Set is_chat_blocked for user

        :param user: User
        :param chat_blocked: Chat blocked
        """

        await self.session.execute(
            update(UserModel)
            .where(
                UserModel.id == user.id
            ).values(
                is_chat_blocked=chat_blocked
            )
        )

        await self.session.commit()
