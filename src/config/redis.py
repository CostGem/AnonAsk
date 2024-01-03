from os import getenv

from pydantic import BaseModel


class RedisConfiguration(BaseModel):
    host: str = getenv("REDIS_HOST")
    username: str = getenv("REDIS_USERNAME")
    password: str = getenv("REDIS_PASSWORD")
    port: int = int(getenv("REDIS_PORT", 6379))
    state_ttl: int = getenv("REDIS_TTL_STATE")
    data_ttl: int = getenv("REDIS_TTL_DATA")
