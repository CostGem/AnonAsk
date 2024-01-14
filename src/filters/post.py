from typing import Any, Union, Dict

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.config import CONFIGURATION


class PostMessageFilter(BaseFilter):
    """Post message filter"""

    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        return message.is_automatic_forward and message.forward_from_chat.id == CONFIGURATION.DATA.channel_id
