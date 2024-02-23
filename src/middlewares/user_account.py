from typing import Callable, Dict, Any, Awaitable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache import LocaleCache
from src.classes.user.user_data import UserData
from src.database.models import UserModel, LocaleModel
from src.database.repositories import UserRepository, LocaleRepository


class UserAccountMiddleware(BaseMiddleware):
    """User account middleware"""

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]
        user_repository: UserRepository = UserRepository(session=session)
        user: Optional[UserModel] = await user_repository.get_by_id(user_id=event.from_user.id)
        locale: Optional[LocaleModel] = None

        if user:
            redis: Redis = data.get("redis")
            locale_cache: LocaleCache = LocaleCache(redis=redis, user_id=user.id)
            locale = await locale_cache.get()

            if not locale:
                locale_repository: LocaleRepository = LocaleRepository(session=session)
                locale: LocaleModel = await locale_repository.get_by_id(locale_id=user.locale_id)
                await locale_cache.set(locale=locale)

        data["user_data"] = UserData(
            repository=user_repository,
            user=user,
            locale=locale
        )

        await handler(event, data)
