from typing import List

from aiogram import Router

from src.handlers.private.user.profile import profile

routers: List[Router] = [
    profile.router
]

router: Router = Router(name="User profile")

router.include_routers(*routers)

__all__ = ["router"]
