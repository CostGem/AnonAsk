from typing import Optional

import environ


@environ.config(prefix="REDIS")
class RedisConfig:
    HOST: str = environ.var()
    USER: Optional[str] = environ.var(default=None)
    PASSWORD: Optional[str] = environ.var(default=None)
    PORT: int = environ.var(default=6379, converter=int)
    STATE_TTL: int = environ.var(default=3600, converter=int)
    DATA_TTL: int = environ.var(default=3600, converter=int)
