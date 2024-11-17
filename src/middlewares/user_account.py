from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import UserModel
from src.database.repositories import UserRepository
from src.dataclasses.user.user_data import UserData


class UserAccountMiddleware(BaseMiddleware):
    """User account middleware"""

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]
        event_from_user: User = data["event_from_user"]

        user_repository: UserRepository = UserRepository(session=session)
        user: UserModel = await user_repository.register(
            user_id=event_from_user.id,
            name=event_from_user.full_name,
            username=event_from_user.username
        )

        data["user_data"] = UserData(
            repository=user_repository,
            user=user
        )

        await handler(event, data)
