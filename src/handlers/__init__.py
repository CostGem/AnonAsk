from typing import List

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import and_f

from src.handlers import private, channel

routers: List[Router] = [
    private.router,
    channel.router
]

router: Router = Router(name="Main")

router.message.filter(
    and_f(
        F.chat.type == ChatType.PRIVATE,
        F.from_user.is_bot.is_(False),
    )
)

router.callback_query.filter(
    and_f(
        F.message.chat.type == ChatType.PRIVATE,
        F.from_user.is_bot.is_(False),
    )
)

router.pre_checkout_query.filter(F.from_user.is_bot.is_(False))

router.include_routers(*routers)

__all__ = ["router"]
