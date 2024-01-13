from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.factories.nickname import SetNicknameFactory
from src.translation.translator import LocalizedTranslator


async def get_nickname_set_menu(translator: LocalizedTranslator) -> InlineKeyboardMarkup:
    """
    Return nickname setting menu

    :param translator: Translator
    """

    set_nickname_menu = InlineKeyboardBuilder()

    set_nickname_menu.button(
        text=translator.get(key="nickname_button_text", is_changing=False),
        callback_data=SetNicknameFactory().pack()
    )

    return set_nickname_menu.as_markup()
