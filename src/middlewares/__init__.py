from aiogram import Dispatcher

from src.middlewares import db, translator, user_account, throttling, album


def register_middlewares(dp: Dispatcher) -> None:
    """Register middlewares"""

    # Throttling
    dp.message.outer_middleware(throttling.ThrottlingMiddleware())
    dp.callback_query.outer_middleware(throttling.ThrottlingMiddleware())
    dp.my_chat_member.outer_middleware(throttling.ThrottlingMiddleware())
    dp.pre_checkout_query.outer_middleware(throttling.ThrottlingMiddleware())

    # Database
    dp.message.outer_middleware(db.DatabaseMiddleware())
    dp.callback_query.outer_middleware(db.DatabaseMiddleware())
    dp.my_chat_member.outer_middleware(db.DatabaseMiddleware())
    dp.pre_checkout_query.outer_middleware(db.DatabaseMiddleware())
    dp.poll_answer.outer_middleware(db.DatabaseMiddleware())

    # User
    dp.message.outer_middleware(user_account.UserAccountMiddleware())
    dp.callback_query.outer_middleware(user_account.UserAccountMiddleware())

    # Translator
    dp.message.outer_middleware(translator.TranslatorMiddleware())
    dp.callback_query.outer_middleware(translator.TranslatorMiddleware())

    # Album
    dp.message.outer_middleware(album.AlbumMiddleware())


__all__ = "register_middlewares"
