from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram import Dispatcher
from aiogram.types import TelegramObject, User, CallbackQuery
from aiolimiter import AsyncLimiter
from cachetools import TTLCache


@dataclass(kw_only=True)
class ThrottlingData:
    limiter: AsyncLimiter
    sent_warning: bool


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self._cache: TTLCache[int, ThrottlingData] = TTLCache(
            maxsize=10_000,
            ttl=0.5,
        )

    def setup(self, dispatcher: Dispatcher) -> None:
        dispatcher.update.outer_middleware(self)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any | None:
        event_user: User = data["event_from_user"]

        if event_user.id not in self._cache:
            limiter = AsyncLimiter(
                max_rate=1,
                time_period=1
            )

            self._cache[event_user.id] = ThrottlingData(
                limiter=limiter,
                sent_warning=False,
            )

        throttling_data = self._cache[event_user.id]

        if not throttling_data.limiter.has_capacity():
            if not throttling_data.sent_warning:
                self._cache[event_user.id].sent_warning = True

                if isinstance(event, CallbackQuery):
                    await event.answer()

            return None

        async with throttling_data.limiter:
            return await handler(event, data)
