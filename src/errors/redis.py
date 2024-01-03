class InvalidRedisKeyError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"Invalid redis key: {key}")


class RedisTTLNotConfiguredError(Exception):
    def __init__(self) -> None:
        super().__init__("TTL need to be preconfigured")
