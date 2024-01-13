from typing import List

from aiogram import Router

from src.handlers.private.user.commands import start

routers: List[Router] = [
    start.router
]

router: Router = Router(name="User commands")

router.include_routers(*routers)

__all__ = ["router"]
