from typing import List

from aiogram import html

from src.translation.translator import LocalizedTranslator
from src.database.models import AchievementModel


async def get_achievements_text(achievements: List[AchievementModel], translator: LocalizedTranslator) -> str:
    """
    Return achievements text

    :param achievements: List of user achievements
    :param translator: Translator
    """

    achievements_text: str = ""

    for index, achievement in enumerate(achievements, start=1):
        achievements_text += html.italic(value=f"{index}. «{achievement.name}»\n")

    return translator.get(
        key="user_achievements_message",
        achievements=achievements_text
    )
