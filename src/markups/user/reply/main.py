from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from src.translation.translator import LocalizedTranslator


def get_main_keyboard(translator: LocalizedTranslator) -> ReplyKeyboardMarkup:
    """
    Returns a main keyboard

    :param translator: Translator
    """

    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    builder.button(
        text=translator.get("schedule_button")
    )
    builder.button(
        text=translator.get("news_button")
    )

    builder.button(
        text=translator.get(key="profile_button")
    )

    return builder.adjust(2, 1).as_markup(resize_keyboard=True)
