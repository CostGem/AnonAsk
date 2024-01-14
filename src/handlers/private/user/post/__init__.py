from typing import List

from aiogram import Router

from src.handlers.private.user.post import comment

routers: List[Router] = [
    comment.router
]

router: Router = Router(name="Commenting")

router.include_routers(*routers)

__all__ = ["router"]
