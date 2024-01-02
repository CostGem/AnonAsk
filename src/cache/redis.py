from redis.asyncio.client import Redis

from config import CONFIGURATION

redis_instance: Redis = Redis(
    host=CONFIGURATION.REDIS.host,
    username=CONFIGURATION.REDIS.username,
    password=CONFIGURATION.REDIS.password,
    port=CONFIGURATION.REDIS.port,
)
