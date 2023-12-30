from dataclasses import dataclass
from os import getenv
from typing import Optional


@dataclass
class RedisConfiguration:
    host: Optional[str] = getenv("REDIS_HOST")
    username: Optional[str] = getenv("REDIS_USERNAME")
    password: Optional[str] = getenv("REDIS_PASSWORD")
    port: Optional[int] = int(getenv("REDIS_PORT", 6379))
    state_ttl: Optional[int] = getenv("REDIS_TTL_STATE")
    data_ttl: Optional[int] = getenv("REDIS_TTL_DATA")
