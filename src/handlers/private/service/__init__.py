from typing import List

from aiogram import Router

from src.handlers.private.service import chat_block, empty_callback

routers: List[Router] = [
    chat_block.router,
    empty_callback.router
]

router: Router = Router(name="Service private routers")

router.include_routers(*routers)

__all__ = ["router"]
