from dataclasses import dataclass
from os import getenv


@dataclass
class DataConfiguration:
    comment_chat_id: int = int(getenv("COMMENT_CHAT_ID"))
    channel_id: int = int(getenv("CHANNEL_ID"))
