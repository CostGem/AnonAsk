from typing import List

from aiogram import Router

from handlers.private import (
    user
)

routers: List[Router] = [
    user.router
]

router: Router = Router(name="private")

__all__ = ["router"]
