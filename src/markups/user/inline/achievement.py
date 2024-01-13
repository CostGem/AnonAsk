from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import AchievementModel
from src.factories.achievement import AchievementDetailsFactory, AchievementsFactory
from src.factories.profile import ProfileFactory
from src.translation.translator import LocalizedTranslator


async def get_achievements_menu(
        translator: LocalizedTranslator,
        achievements: List[AchievementModel]
) -> InlineKeyboardMarkup:
    """
    Return achievements menu

    :param achievements: User achievements
    :param translator: Translator
    """

    achievements_menu = InlineKeyboardBuilder()

    for index, achievement in enumerate(achievements, start=1):
        achievements_menu.button(
            text=f"{index}",
            callback_data=AchievementDetailsFactory(achievement_id=achievement.id).pack()
        )

    achievements_menu.adjust(4)

    achievements_menu.row(
        InlineKeyboardButton(
            text=translator.get(key="back_button_text"),
            callback_data=ProfileFactory().pack()
        )
    )

    return achievements_menu.as_markup()


async def get_to_achievements_menu(translator: LocalizedTranslator) -> InlineKeyboardMarkup:
    """
    Return back to achievements menu

    :param translator: Translator
    """

    to_achievements_menu = InlineKeyboardBuilder()

    to_achievements_menu.button(
        text=translator.get(key="back_button_text"),
        callback_data=AchievementsFactory().pack()
    )

    return to_achievements_menu.as_markup()
