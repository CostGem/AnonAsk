from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.translation.translator import LocalizedTranslator


async def get_main_keyboard(translator: LocalizedTranslator) -> ReplyKeyboardMarkup:
    """
    Return main menu keyboard

    :param translator: Translator
    """

    main_keyboard = ReplyKeyboardBuilder()

    main_keyboard.button(text=translator.get(key="timetable_button_text"))
    main_keyboard.button(text=translator.get(key="profile_button_text"))

    return main_keyboard.as_markup(resize_keyboard=True)


async def get_back_to_main_keyboard(translator: LocalizedTranslator) -> ReplyKeyboardMarkup:
    """
    Return back to main menu keyboard

    :param translator: Translator
    """

    back_to_main_keyboard = ReplyKeyboardBuilder()

    back_to_main_keyboard.button(
        text=translator.get(key="back_to_main_button_text")
    )

    return back_to_main_keyboard.as_markup(resize_keyboard=True)
