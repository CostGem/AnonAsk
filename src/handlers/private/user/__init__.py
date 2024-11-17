from typing import List

from aiogram import Router

from src.handlers.private.user import commands, anon_message

routers: List[Router] = [
    commands.router,
    anon_message.router
]

router: Router = Router(name="User private routers")

router.include_routers(*routers)

__all__ = ["router"]
