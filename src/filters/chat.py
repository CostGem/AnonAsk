from typing import Any, Union, Dict

from aiogram.filters import BaseFilter


class ChatTypeFilter(BaseFilter):
    async def __call__(self, *args: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        pass
