from aiogram import Router
from typing import List
from src.handlers.private import (
    user
)

routers: List[Router] = [
    user.router
]

router: Router = Router(name="private")

__all__ = ["router"]
