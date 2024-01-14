from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from src.classes.user.user_data import UserData
from src.enums import Role
from src.translation.translator import LocalizedTranslator


class AdminFilter(BaseFilter):
    """Admin filter"""

    async def __call__(
            self,
            message:
            Union[Message, CallbackQuery],
            translator: LocalizedTranslator,
            user_data: UserData
    ) -> bool:
        return user_data.role.level == Role.ADMIN
