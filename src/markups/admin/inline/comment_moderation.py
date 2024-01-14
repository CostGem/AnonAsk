from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.factories.comment_moderation import CommentDeleteFactory, CommentUserBanFactory
from src.translation.translator import LocalizedTranslator


async def get_comment_moderation_menu(comment_id: int, translator: LocalizedTranslator) -> InlineKeyboardMarkup:
    """
    Return comment moderation menu

    :param comment_id: Comment ID
    :param translator: Translator
    """

    comment_moderation_menu = InlineKeyboardBuilder()

    comment_moderation_menu.button(
        text=translator.get(key="delete_comment_button_text"),
        callback_data=CommentDeleteFactory(comment_id=comment_id).pack()
    )

    comment_moderation_menu.button(
        text=translator.get(key="ban_comment_user_button_text"),
        callback_data=CommentUserBanFactory(comment_id=comment_id).pack()
    )

    return comment_moderation_menu.adjust(1).as_markup()
