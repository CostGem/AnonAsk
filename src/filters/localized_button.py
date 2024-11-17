from typing import Optional, Any, Dict, Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.translation.translator import LocalizedTranslator


class LocalizedButtonFilter(BaseFilter):
    """Localized reply keyboard button filter"""

    __translation_key: Optional[str] = None
    __translations: Optional[Dict[str, str]] = None

    def __init__(self, key: str) -> None:
        self.__translation_key = key
        self.__translations = {}

    async def __call__(self, message: Message, translator: LocalizedTranslator) -> Union[bool, Dict[str, Any]]:
        button_translated_text: Optional[str] = self.__translations.get(self.__translation_key)

        if not button_translated_text:
            button_translated_text = translator.get(key=self.__translation_key)
            self.__translations[translator.locale] = button_translated_text

        return message.text == button_translated_text
