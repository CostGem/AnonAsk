from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.classes.user.user_data import UserData
from src.database.models import LocaleModel
from src.factories.locale import SetLocaleFactory
from src.factories.profile import ProfileFactory
from src.translation.translator import LocalizedTranslator


async def get_locales_list_menu(
        user_data: UserData,
        locales: List[LocaleModel],
        translator: LocalizedTranslator
) -> InlineKeyboardMarkup:
    """
    Return locale selection menu

    :param user_data: User data
    :param locales: List of locales
    :param translator: Translator
    """

    locales_menu = InlineKeyboardBuilder()
    user_locale = user_data.user.locale_id if user_data.locale else None

    for locale in locales:
        locales_menu.button(
            text=translator.get(
                key="locales_list_button_text",
                emoji=locale.emoji,
                name=locale.name,
                is_user_locale=locale.id == user_locale
            ),
            callback_data=SetLocaleFactory(locale_id=locale.id).pack()
        )

    locales_menu.button(
        text=translator.get(key="back_button_text"),
        callback_data=ProfileFactory().pack()
    )

    locales_menu.adjust(1)

    return locales_menu.as_markup()
