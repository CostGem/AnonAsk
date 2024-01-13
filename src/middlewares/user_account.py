from typing import Callable, Dict, Any, Awaitable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.classes.user.user_data import UserData
from src.database.models import UserModel
from src.database.repositories.user import UserRepository


class UserAccountMiddleware(BaseMiddleware):
    """User account middleware"""

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        session:  AsyncSession = data["session"]
        user_repository: UserRepository = UserRepository(session=session)
        user: Optional[UserModel] = await user_repository.get(ident=event.from_user.id)

        data["user_data"] = UserData(repository=user_repository, user=user)

        return await handler(event, data)
