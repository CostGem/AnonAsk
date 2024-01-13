from typing import Dict, Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.translation.translator import LocalizedTranslator


class KeyboardButtonFilter(BaseFilter):
    """Localized button text filter"""

    __button_text_key: str
    __translations: Dict[str, str]

    def __init__(self, key: str) -> None:
        """"
        :param key: Button key
        """

        self.__button_text_key = key
        self.__translations = {}

    async def __call__(self, message: Message, translator: LocalizedTranslator) -> bool:
        button_translated_text: Optional[str] = self.__translations.get(self.__button_text_key)

        if not button_translated_text:
            button_translated_text = translator.get(key=self.__button_text_key)
            self.__translations[translator.locale] = button_translated_text

        return message.text == button_translated_text
