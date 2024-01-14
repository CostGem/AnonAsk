from typing import List

from aiogram import Router

from src.handlers.private.user import commands, profile, post, misc

routers: List[Router] = [
    misc.router,
    commands.router,
    profile.router,
    post.router
]

router: Router = Router(name="User")

router.include_routers(*routers)

__all__ = ["router"]
