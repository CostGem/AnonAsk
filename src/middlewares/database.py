from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DatabaseMiddleware(BaseMiddleware):
    """Database session to handlers"""

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        session_maker: async_sessionmaker = data["database_session_maker"]
        async with session_maker() as session:
            data["session"] = session
            return await handler(event, data)
