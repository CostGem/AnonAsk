from typing import List

from aiogram import Router

from src.handlers.private.user import commands

routers: List[Router] = [
    commands.router
]

router: Router = Router(name="User private routers")

router.include_routers(*routers)

__all__ = ["router"]
