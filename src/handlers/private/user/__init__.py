from typing import List

from aiogram import Router

from src.handlers.private.user import main_start

routers: List[Router] = [
    main_start.router
]

router: Router = Router(name="user")

router.include_routers(*routers)

__all__ = ["router"]
