from dataclasses import dataclass
from os import getenv
from typing import Optional

from aiogram.client.session.base import BaseSession
from aiogram.enums import ParseMode


@dataclass
class BotConfiguration:
    # Base values
    token: Optional[str] = None
    parse_mode: ParseMode = ParseMode.HTML
    session: Optional[BaseSession] = None
    disable_web_page_preview: Optional[bool] = None
    protect_content: Optional[bool] = None

    # Webhook
    webhook_url: Optional[str] = None
    webhook_endpoint: Optional[str] = None
    webhook_host: Optional[str] = None
    webhook_port: int = 8000
    nginx_host: Optional[str] = None

    def __init__(self) -> None:
        self.load_from_env()

    def load_from_env(self) -> None:
        """Load data from env file"""

        self.token = getenv("BOT_TOKEN")
        self.webhook_url = getenv("BOT_WEBHOOK_URL")
        self.webhook_endpoint = getenv("BOT_WEBHOOK_ENDPOINT")
        self.webhook_host = getenv("BOT_WEBHOOK_HOST")
        self.webhook_port = int(getenv("BOT_WEBHOOK_PORT", 8000))
        self.nginx_host = getenv("NGINX_HOST")
