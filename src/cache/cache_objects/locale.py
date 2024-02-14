from typing import Any, Optional

from redis.asyncio import Redis

from src.cache.cache_models import LocaleCacheModel
from src.cache.cache_objects.base import BaseCache
from src.database.models import LocaleModel


class LocaleCache(BaseCache):
    """Locale cache"""

    prefix: str = "locale"

    def __init__(self, redis: Redis, user_id: int) -> None:
        super().__init__(redis=redis, item_id=user_id, ttl=300)

    async def set(self, value: LocaleCacheModel) -> None:
        await super().set(value=value.to_json())

    async def get(self) -> Optional[LocaleModel]:
        raw_locale = await super().get()

        if not raw_locale:
            return None

        return LocaleModel(
            **LocaleCacheModel.from_json(raw_locale).__dict__
        )
