from aiogram import Router
from typing import List
from src.handlers.private.user import main_start

routers: List[Router] = [
    main_start.router
]

router: Router = Router(name="user")

__all__ = ["router"]
