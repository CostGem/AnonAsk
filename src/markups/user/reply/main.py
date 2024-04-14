from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from src.translation.translator import LocalizedTranslator


async def get_main_keyboard(translator: LocalizedTranslator) -> ReplyKeyboardMarkup:
    """
    Returns a main keyboard

    :param translator: Translator
    """

    main_keyboard: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    main_keyboard.button(
        text=translator.get("schedule_button_text")
    )
    main_keyboard.button(
        text=translator.get("news_button_text")
    )

    main_keyboard.button(
        text=translator.get("profile_button_text")
    )

    return main_keyboard.adjust(1).as_markup(resize_keyboard=True)
