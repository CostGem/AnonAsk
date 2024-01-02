from typing import List
from aiogram import Router

routers: List[Router] = [

]

router: Router = Router(name="main")
router.include_routers(*routers)

__all__ = ["router"]
