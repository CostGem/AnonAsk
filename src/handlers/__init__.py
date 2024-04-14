from typing import List

from aiogram import Router, F
from aiogram.enums import ChatType

from src.handlers import private

routers: List[Router] = [
    private.router
]

router: Router = Router(name="Main router")

router.message.filter(F.chat.type == ChatType.PRIVATE)
router.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)

router.include_routers(*routers)

__all__ = ["router"]
