from typing import List

from aiogram import Router

from src.handlers.private import (
    user,
    admin
)

routers: List[Router] = [
    user.router,
    admin.router
]

router: Router = Router(name="Private")

router.include_routers(*routers)

__all__ = ["router"]
