from typing import List

from aiogram import Router, F
from aiogram.enums import ChatType

from src.handlers.private import user, service

routers: List[Router] = [
    user.router,
    service.router
]

router: Router = Router(name="Private routers")

router.message.filter(F.chat.type == ChatType.PRIVATE)
router.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)

router.include_routers(*routers)

__all__ = ["router"]
