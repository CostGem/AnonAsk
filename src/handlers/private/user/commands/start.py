from typing import Optional

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User
from aiogram.utils.deep_linking import encode_payload
from aiogram.utils.payload import decode_payload

from src.database.models import UserModel
from src.dataclasses.user.user_data import UserData
from src.states.anonim import AnonimMessageState
from src.translation.translator import LocalizedTranslator
from src.utils.user.link import get_anonim_link

router: Router = Router(name="Start command")


@router.message(Command(commands="start", magic=~F.args))
async def start(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator
) -> None:
    await state.clear()

    await message.answer(
        text=translator.get(
            key="welcome_message",
            link=await get_anonim_link(user_id=message.from_user.id)
        )
    )


@router.message(Command(commands="start", magic=F.args))
async def anonim_message_start(
        message: Message,
        command: CommandObject,
        state: FSMContext,
        translator: LocalizedTranslator,
        user_data: UserData
) -> None:
    await state.clear()

    try:
        decoded_args: str = decode_payload(payload=command.args)
    except Exception as ex:
        await message.answer(
            text=translator.get(
                key="invalid_start_link_message"
            )
        )
        return

    user_id: int = int(decoded_args)
    user: Optional[UserModel] = await user_data.repository.get_by_id(user_id=user_id)

    if user and user.is_chat_blocked:
        await message.answer(
            text=translator.get(
                key="user_is_blocked_message"
            )
        )
        return

    await state.set_state(state=AnonimMessageState.MESSAGE)
    await state.update_data(user_id=user_id)

    await message.answer(
        text=translator.get(
            key="send_anonim_message_message"
        )
    )
