from aiogram import Dispatcher

from src.middlewares import db, translator


def register_middlewares(dp: Dispatcher) -> None:
    """
    The function `register_middlewares` adds a database middleware to various types of messages and
    queries in a Telegram bot.

    :param dp: The `dp` parameter is an instance of the `Dispatcher` class. The `Dispatcher` class is
    responsible for handling incoming updates and routing them to the appropriate handlers
    :type dp: Dispatcher
    """
    # database
    dp.message.outer_middleware(db.DatabaseMiddleware())
    dp.callback_query.outer_middleware(db.DatabaseMiddleware())
    dp.my_chat_member.outer_middleware(db.DatabaseMiddleware())
    dp.pre_checkout_query.outer_middleware(db.DatabaseMiddleware())
    dp.poll_answer.outer_middleware(db.DatabaseMiddleware())

    # translator
    dp.message.middleware(translator.TranslatorMiddleware())
    dp.callback_query.middleware(translator.TranslatorMiddleware())


__all__ = "register_middlewares"
