from redis.asyncio import Redis

from src.cache.cache_objects.base import BaseCache


class LocaleCache(BaseCache):
    """Locale cache"""

    prefix: str = "locale"

    def __init__(self, redis: Redis, user_id: int) -> None:
        super().__init__(redis=redis, item_id=user_id, ttl=300)
