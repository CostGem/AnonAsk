from typing import List

from aiogram import Router

from src.handlers import private

routers: List[Router] = [
    private.router
]

router: Router = Router(name="Main router")

router.include_routers(*routers)

__all__ = ["router"]
