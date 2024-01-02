from typing import List, Union, Optional

from config import CONFIGURATION
from redis.asyncio.client import Redis
from termcolor import cprint


class BasicCache:
    """Basic cache class

    ### !! Should be inherited

    ### Example

    class ExampleCache(BasicCache):

        ttl: int = 5 - time to live
        prefix: str = "example"
        use_pointer: bool = False - pointer cache can have two keys
            * item_id - primary key (cache data will be stored by that one)
            * pointer_id - secondary key (at first reads primary key from cache and then reads the data from base cache)

    """

    # configurable options
    ttl: int = 60
    prefix: str

    __redis: Redis
    __item_id: Optional[Union[str, int]]
    __pointer_id: Optional[Union[str, int]] = None
    __pointer_key: Optional[str] = None

    __cache_prefix_list: List[str] = []

    def __init__(
            self,
            redis: Redis,
            item_id: Optional[Union[str, int]] = None,
            ttl: Optional[int] = None,
    ) -> None:
        """inital function"""

        self.__redis = redis
        self.__item_id = item_id
        self.__ttl = ttl if ttl else self.__ttl

        self.__validate_keys()

    def __init_subclass__(cls, is_cache_extension: bool = False, **kwargs):
        super().__init_subclass__(**kwargs)

        if not is_cache_extension:
            if not hasattr(cls, "ttl"):
                raise ValueError("TTL need to be preconfigured")
            else:
                cls.__ttl = cls.ttl

            if not hasattr(cls, "prefix"):
                raise ValueError("Prefix is not configured")
            else:
                cls.__prefix = cls.prefix

            if cls.prefix in BasicCache.__cache_prefix_list:
                raise ValueError(
                    "You have set the prefix, that already used in another cache class object"
                )
            else:
                BasicCache.__cache_prefix_list.append(cls.prefix)

    async def get_from_cache(self) -> Optional[str]:
        """Get a cached value from redis"""

        if key := await self.__get_redis_key():
            if redis_value := await self.__redis.get(name=key):
                if CONFIGURATION.IS_DEVELOPMENT:
                    cprint(f"{self.prefix}:{self.__item_id} cached", "green")
                return redis_value.decode()
            else:
                return None

    async def set_cache_value(self, value: str) -> None:
        """Set a value to redis"""

        if redis_key := await self.__get_redis_key():
            if await self.get_from_cache() != value:
                await self.__redis.set(ex=self.__ttl, name=redis_key, value=value)
        else:
            raise ValueError("Invalid redis_key")

    async def delete_cache_value(self) -> None:
        """cache that supports storing json data"""

        if self.__item_id:
            if redis_key := await self.__get_redis_key():
                if await self.__redis.get(redis_key):
                    await self.__redis.delete(redis_key)

    async def delete(self) -> None:
        return await self.delete_cache_value()
