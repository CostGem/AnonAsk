from typing import List

from aiogram import Router

from src.handlers.private.user.profile import profile, locale, status, nickname, achievement

routers: List[Router] = [
    profile.router,
    locale.router,
    status.router,
    nickname.router,
    achievement.router
]

router: Router = Router(name="User profile")

router.include_routers(*routers)

__all__ = ["router"]
