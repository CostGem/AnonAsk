from dataclasses import dataclass
from os import getenv
from typing import Optional


@dataclass
class RedisConfiguration:
    host: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    port: int = 6379
    state_ttl: Optional[int] = None
    data_ttl: Optional[int] = None

    def __init__(self) -> None:
        self.load_from_env()

    def load_from_env(self) -> None:
        """Load data from env file"""

        self.host = getenv("REDIS_HOST")
        self.username = getenv("REDIS_USERNAME")
        self.password = getenv("REDIS_PASSWORD")
        self.port = int(getenv("REDIS_PORT", 6379))
        self.state_ttl = getenv("REDIS_TTL_STATE")
        self.data_ttl = getenv("REDIS_TTL_DATA")
