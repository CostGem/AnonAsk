from contextlib import suppress
from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.enums import MessageEntityType
from aiogram.filters.command import CommandException
from aiogram.types import TelegramObject, Message
from aiogram.utils.deep_linking import decode_payload

from src.dataclasses.service.decoded_command import DecodedCommand


class CommandDecodeMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any],
    ) -> Any:
        if message.entities and message.entities[0].type == MessageEntityType.BOT_COMMAND:
            try:
                full_command, *args = message.text.split(maxsplit=1)
            except ValueError:
                raise CommandException("Not enough values to unpack")

            command_args: Optional[str] = args[0] if args else None

            if command_args:
                with suppress(UnicodeDecodeError):
                    command_args = decode_payload(args[0])

                if ":" in command_args:
                    command, args = command_args.split(":", maxsplit=1)

                    data["decoded_command"] = DecodedCommand(
                        command=command,
                        args=args
                    )

        await handler(message, data)
