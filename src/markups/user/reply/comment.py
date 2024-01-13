from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.translation.translator import LocalizedTranslator


async def get_cancel_commenting_keyboard(translator: LocalizedTranslator) -> ReplyKeyboardMarkup:
    """
    Return commenting keyboard

    :param translator: Translator
    """

    cancel_commenting_keyboard = ReplyKeyboardBuilder()

    cancel_commenting_keyboard.button(
        text=translator.get(key="cancel_commenting_button_text")
    )

    return cancel_commenting_keyboard.as_markup(resize_keyboard=True)
