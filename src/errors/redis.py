class InvalidRedisKeyError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"Invalid redis key: {key}")


class RedisTTLNotConfiguredError(Exception):
    def __init__(self) -> None:
        super().__init__("TTL need to be preconfigured")


class RedisPrefixNotConfiguredError(Exception):
    def __init__(self) -> None:
        super().__init__("Prefix need to be preconfigured")


class RedisPrefixAlreadyUsedError(Exception):
    def __init__(self, prefix: str) -> None:
        super().__init__(f"Prefix '{prefix}' already used in another cache class object")
