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
    """
    The `BasicCache` class is a basic implementation of a cache that uses Redis as the underlying
    storage and provides methods for getting, setting, and deleting cache values.
    """

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
        """
        The `__init_subclass__` function is used to initialize subclasses of a class and perform some
        validation checks on the subclass attributes.

        :param cls: The `cls` parameter refers to the subclass that is being initialized. In other words, it
        represents the class that is inheriting from the `BasicCache` class
        :param is_cache_extension: The `is_cache_extension` parameter is a boolean flag that indicates
        whether the class being defined is a cache extension or not. If it is set to `True`, it means that
        the class is a cache extension and the code inside the `if` block will not be executed, defaults to
        False
        :type is_cache_extension: bool (optional)
        """
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
        """Get a redis key

        * key can be constructed using configured item_id value
        * key can be constructed via loading cached item_id value

        """

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
                return redis_value.decode()

    async def set(self, value: str) -> None:
        """
        Sets a value in a cache if the redis key is valid and the value is
        different from the current value in the cache.

        :param value: The `value` parameter is a string that represents the value to be stored in the cache
        :type value: str
        """

        if redis_key := await self.__get_redis_key():
            if await self.get() != value:
                await self.__redis.set(ex=self.__ttl, name=redis_key, value=value)
        else:
            raise InvalidRedisKeyError(key=redis_key)

    async def delete(self) -> None:
        """Delete a value from a Redis cache"""

        if redis_key := await self.__get_redis_key():
            if await self.__redis.get(name=redis_key):
                await self.__redis.delete(redis_key)
