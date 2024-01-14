from typing import List

from aiogram import Router

from src.filters import AdminFilter
from src.handlers.private.admin import comment_moderation, file_info, timetable

routers: List[Router] = [
    comment_moderation.router,
    file_info.router,
    timetable.router
]

router: Router = Router(name="Admin")

router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())

router.include_routers(*routers)

__all__ = ["router"]
