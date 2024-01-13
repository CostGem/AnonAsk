from typing import List

from aiogram import Router

from src.handlers.private.user import commands, profile

routers: List[Router] = [
    commands.router,
    profile.router
]

router: Router = Router(name="User")

router.include_routers(*routers)

__all__ = ["router"]
