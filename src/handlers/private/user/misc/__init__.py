from typing import List

from aiogram import Router

from src.handlers.private.user.misc import back_to_main, timetable, user_status

routers: List[Router] = [
    back_to_main.router,
    timetable.router,
    user_status.router,
]

router: Router = Router(name="Misc")

router.include_routers(*routers)

__all__ = ["router"]
