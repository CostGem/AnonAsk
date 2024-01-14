import logging

from aiogram import Bot

from src.config import CONFIGURATION
from src.database.models import CommentModel
from src.database.repositories import CommentRepository


async def delete_comments(comment: CommentModel, comment_repository: CommentRepository, bot: Bot) -> None:
    """
    Delete comment and his replies

    :param comment: Comment
    :param comment_repository: CommentRepository
    :param bot: Bot
    """

    child_comments = await comment_repository.get_child_comments(parent_comment_id=comment.id)
    comments_ids = [comment.id, *[child_comment.message_id for child_comment in child_comments]]

    try:
        await bot.delete_messages(
            chat_id=CONFIGURATION.DATA.comment_chat_id,
            message_ids=comments_ids
        )
    except Exception as error:
        logging.error(error)
