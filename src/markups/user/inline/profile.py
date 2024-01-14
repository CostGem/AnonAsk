from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import UserModel
from src.factories.achievement import AchievementsFactory
from src.factories.nickname import SetNicknameFactory
from src.factories.profile import ProfileFactory
from src.factories.status import StatusesFactory
from src.translation.translator import LocalizedTranslator


async def get_profile_menu(user: UserModel, translator: LocalizedTranslator) -> InlineKeyboardMarkup:
    """
    Return profile menu

    :param user: User
    :param translator: Translator
    """

    profile_menu = InlineKeyboardBuilder()

    profile_menu.button(
        text=translator.get(key="nickname_button_text", is_changing=bool(user.nickname)),
        callback_data=SetNicknameFactory().pack()
    )

    profile_menu.button(
        text=translator.get(key="achievements_button_text"),
        callback_data=AchievementsFactory().pack()
    )

    profile_menu.button(
        text=translator.get(key="statuses_button_text"),
        callback_data=StatusesFactory().pack()
    )

    profile_menu.adjust(1)

    return profile_menu.as_markup()


async def get_to_profile_menu(translator: LocalizedTranslator) -> InlineKeyboardMarkup:
    """
    Return back to profile menu

    :param translator: Translator
    """

    to_profile_menu = InlineKeyboardBuilder()

    to_profile_menu.button(
        text=translator.get(key="back_button_text"),
        callback_data=ProfileFactory().pack()
    )

    return to_profile_menu.as_markup()
