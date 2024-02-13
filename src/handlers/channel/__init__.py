from typing import List

from aiogram import Router

from src.handlers.channel import service

routers: List[Router] = [
    service.router
]

router: Router = Router(name="Channel routers")

router.include_routers(*routers)

__all__ = ["router"]
