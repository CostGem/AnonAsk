from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.factories.profile import ProfileFactory
from src.factories.status import SetStatusFactory
from src.translation.translator import LocalizedTranslator
from src.database.models import StatusModel


async def get_statuses_menu(
        user_status: StatusModel,
        translator: LocalizedTranslator,
        statuses: List[StatusModel]
) -> InlineKeyboardMarkup:
    """
    Return statuses menu

    :param user_status: Current user status
    :param statuses: List of statuses
    :param translator: Translator
    """

    statuses_menu = InlineKeyboardBuilder()

    for status in statuses:
        statuses_menu.button(
            text=translator.get(
                key="statuses_list_button_text",
                emoji=status.emoji,
                is_user_status=status.id == user_status.id
            ),
            callback_data=SetStatusFactory(status_id=status.id).pack()
        )

    statuses_menu.adjust(4)

    statuses_menu.row(
        InlineKeyboardButton(
            text=translator.get(key="back_button_text"),
            callback_data=ProfileFactory().pack()
        )
    )

    return statuses_menu.as_markup()
