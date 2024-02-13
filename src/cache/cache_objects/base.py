from typing import Any, List, Union, Optional

from redis.asyncio.client import Redis
from termcolor import cprint

from src.config import CONFIGURATION
from src.errors.redis import (
    InvalidRedisKeyError,
    RedisTTLNotConfiguredError,
    RedisPrefixNotConfiguredError,
    RedisPrefixAlreadyUsedError
)


class BasicCache:
    """Base class for cache"""

    ttl: int = 60
    prefix: str

    __redis: Redis
    __item_id: Optional[Union[str, int]]
    __cache_prefix_list: List[str] = []

    def __init__(
            self,
            redis: Redis,
            item_id: Optional[Union[str, int]] = None,
            ttl: Optional[int] = None,
    ) -> None:
        self.__redis = redis
        self.__item_id = item_id
        self.__ttl = ttl if ttl else self.__ttl

    def __init_subclass__(cls, is_cache_extension: bool = False, **kwargs):
        """Initialize subclass"""

        super().__init_subclass__(**kwargs)

        if not is_cache_extension:
            if not hasattr(cls, "ttl"):
                raise RedisTTLNotConfiguredError()
            else:
                cls.__ttl = cls.ttl

            if not hasattr(cls, "prefix"):
                raise RedisPrefixNotConfiguredError()
            else:
                cls.__prefix = cls.prefix

            if cls.prefix in BasicCache.__cache_prefix_list:
                raise RedisPrefixAlreadyUsedError(prefix=cls.prefix)
            else:
                BasicCache.__cache_prefix_list.append(cls.prefix)

    async def __get_redis_key(self) -> Optional[str]:
        """Redis key builder"""

        return f"{self.__prefix}:{self.__item_id}"

    async def get(self) -> Optional[Any]:
        """Get a cached value from redis"""

        if key := await self.__get_redis_key():
            if redis_value := await self.__redis.get(name=key):
                if CONFIGURATION.IS_DEVELOPMENT:
                    cprint(
                        f"{self.prefix}:{self.__item_id} received from the cache",
                        "green",
                    )
                return redis_value

    async def set(self, value: Union[bytes, memoryview, str, int, float]) -> None:
        """Set cache value"""

        if redis_key := await self.__get_redis_key():
            await self.__redis.set(ex=self.__ttl, name=redis_key, value=value)
        else:
            raise InvalidRedisKeyError(key=redis_key)

    async def delete(self) -> None:
        """Delete a value from cache"""

        redis_key: str = await self.__get_redis_key()
        await self.__redis.delete(redis_key)
