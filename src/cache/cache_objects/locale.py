from json import loads
from typing import Optional

from redis.asyncio import Redis

from src.cache.cache_models import LocaleCacheModel
from src.cache.cache_objects.base import JSONCache
from src.database.models import LocaleModel


class LocaleCache(JSONCache):
    """Locale cache"""

    prefix: str = "locale"

    def __init__(self, redis: Redis, user_id: int) -> None:
        super().__init__(redis=redis, item_id=user_id, ttl=300)

    async def set(self, locale: LocaleModel) -> None:
        """Set locale to json cache"""

        await super().set(
            value=LocaleCacheModel(
                emoji=locale.emoji,
                name=locale.name,
                code=locale.code
            ).to_json()
        )

    async def get(self) -> Optional[LocaleModel]:
        """Get locale from json cache"""

        raw_json = await super().get()

        if not raw_json:
            return None

        return LocaleModel(
            **loads(raw_json)
        )
