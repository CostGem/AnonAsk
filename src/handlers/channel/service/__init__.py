from typing import List

from aiogram import Router

from src.handlers.channel.service import post

routers: List[Router] = [
    post.router
]

router: Router = Router(name="Service")

router.include_routers(*routers)

__all__ = ["router"]
