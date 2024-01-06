from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from src.translation.translator import LocalizedTranslator, TranslatorManager


class TranslatorMiddleware(BaseMiddleware):
    """
    The `TranslatorMiddleware` class is a middleware that sets up a translator based on the user's
    language code and adds it to the data dictionary for further processing.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data["event_from_user"]

        locale: str = user.language_code

        translator: LocalizedTranslator = TranslatorManager().get_translator(
            locale=locale
        )

        data["translator"] = translator

        return await handler(event, data)
