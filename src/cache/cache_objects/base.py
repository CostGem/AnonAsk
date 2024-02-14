import logging
from json import loads
from typing import Any, List, Union, Optional, TypeVar, Generic

from redis.asyncio.client import Redis

from src.errors.redis import (
    InvalidRedisKeyError,
    RedisTTLNotConfiguredError,
    RedisPrefixNotConfiguredError,
    RedisPrefixAlreadyUsedError
)

JSONModel = TypeVar("JSONModel")
CacheModel = TypeVar("CacheModel")


class BaseCache:
    """Base class for cache"""

    ttl: int = 60
    prefix: str
    separator: str = ":"

    __redis: Redis
    __item_id: Optional[Union[str, int]]
    __cache_prefixes_list: List[str] = []

    def __init__(self, redis: Redis, item_id: Optional[Union[str, int]] = None, ttl: Optional[int] = None) -> None:
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
                cls.prefix = cls.prefix

            if cls.prefix in BaseCache.__cache_prefixes_list:
                raise RedisPrefixAlreadyUsedError(prefix=cls.prefix)
            else:
                BaseCache.__cache_prefixes_list.append(cls.prefix)

    async def __get_redis_key(self) -> Optional[str]:
        """Redis key builder"""

        return f"{self.prefix}{self.separator}{self.__item_id}" if self.__item_id else self.prefix

    async def get(self) -> Optional[Any]:
        """Get a cached value from redis"""

        if key := await self.__get_redis_key():
            if redis_value := await self.__redis.get(name=key):
                logging.debug(f"{self.prefix}:{self.__item_id} received from the cache")
                return redis_value

    async def set(self, value: Any) -> None:
        """Set cache value"""

        if redis_key := await self.__get_redis_key():
            await self.__redis.set(ex=self.__ttl, name=redis_key, value=value)
        else:
            raise InvalidRedisKeyError(key=redis_key)

    async def delete(self) -> None:
        """Delete a value from cache"""

        redis_key: str = await self.__get_redis_key()
        await self.__redis.delete(redis_key)


class JSONCache(BaseCache, Generic[JSONModel, CacheModel]):
    """JSON cache"""

    def __init__(self, redis: Redis, item_id: Optional[Union[str, int]] = None, ttl: Optional[int] = None) -> None:
        super().__init__(redis=redis, item_id=item_id, ttl=ttl)

    async def set(self, value: JSONModel) -> None:
        """Set a value as json"""

        await super().set(value=value.to_json())

    async def get(self) -> Optional[CacheModel]:
        """Get converting model from json cache"""

        json_model = await super().get()

        if not json_model:
            return None

        return CacheModel(
            **loads(json_model)
        )
