from aiogram import Router
from typing import List

routers: List[Router] = [
    Router()
]

router: Router = Router(name="user")

__all__ = ["router"]
