from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dependency_injector.wiring import Provide

from src.containers.app import AppContainer
from src.enums.service.locale import LocalesEnum
from src.translation.translator import LocalizedTranslator, TranslatorManager


class TranslatorMiddleware(BaseMiddleware):
    """Translator middleware"""

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        translator: LocalizedTranslator = TranslatorManager().get_translator(locale=LocalesEnum.RU)

        data["translator"] = translator

        await handler(event, data)
