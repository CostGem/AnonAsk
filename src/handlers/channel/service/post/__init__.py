from typing import List

from aiogram import Router

from src.handlers.channel.service.post import post_edit

routers: List[Router] = [
    post_edit.router
]

router: Router = Router(name="Post handling")

router.include_routers(*routers)

__all__ = ["router"]
