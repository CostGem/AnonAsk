from typing import List

from aiogram import Router

from src.handlers import private, channel

routers: List[Router] = [
    private.router,
    channel.router
]

router: Router = Router(name="Main router")

router.include_routers(*routers)

__all__ = ["router"]
