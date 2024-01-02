from dataclasses import dataclass
from os import getenv
from typing import Optional

from aiogram.client.session.base import BaseSession
from aiogram.enums import ParseMode


@dataclass
class BotConfiguration:
    token: Optional[str] = getenv("BOT_TOKEN")
    parse_mode: ParseMode = ParseMode.HTML
    session: Optional[BaseSession] = None
    disable_web_page_preview: Optional[bool] = None
    protect_content: Optional[bool] = None

    # webhook
    webhook_url: Optional[str] = getenv("BOT_WEBHOOK_URL")
    webhook_endpoint: Optional[str] = getenv("BOT_WEBHOOK_ENDPOINT")
    webhook_host: Optional[str] = getenv("BOT_WEBHOOK_HOST")
    webhook_port: Optional[str] = getenv("BOT_WEBHOOK_PORT")
    nginx_host: Optional[str] = getenv("NGINX_HOST")
