from contextlib import suppress

import emoji
from aiogram import Router, F, html
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes.user.user_data import UserData
from src.database.repositories import PostRepository, CommentRepository
from src.factories.nickname import SetNicknameFactory
from src.markups.user.reply.comment import get_cancel_commenting_keyboard
from src.markups.user.reply.main_menu import get_back_to_main_keyboard, get_main_keyboard
from src.states import NicknameState, CommentState
from src.translation.translator import LocalizedTranslator

router = Router(name="Nickname router")


@router.callback_query(SetNicknameFactory.filter(), StateFilter(None))
async def set_nickname(
        call: CallbackQuery,
        state: FSMContext,
        translator: LocalizedTranslator
) -> None:
    with suppress(TelegramBadRequest):
        await call.message.delete()

    await state.set_state(state=NicknameState.NICKNAME)

    back_to_main_keyboard = await get_back_to_main_keyboard(translator=translator)
    await call.message.answer(
        text=translator.get(key="set_nickname_message"),
        reply_markup=back_to_main_keyboard
    )


@router.message(F.text, StateFilter(NicknameState.NICKNAME))
async def enter_nickname(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    if len(message.text) > 12:
        await message.answer(
            text=translator.get(key="nickname_length_to_long_message")
        )
        return

    if emoji.emoji_count(string=message.html_text, unique=False) > 0:
        await message.answer(
            text=translator.get(key="emoji_are_prohibited_in_nickname_message")
        )
        return

    if await user_data.repository.nickname_is_taken(nickname=message.text.lower()):
        await message.answer(
            text=translator.get(key="nickname_is_taken_message")
        )
        return

    await user_data.repository.set_nickname(user=user_data.user, nickname=message.text)

    data = await state.get_data()
    post_id = data.get("post_id")

    if not post_id:
        await state.clear()
        main_keyboard = await get_main_keyboard(translator=translator)
        await message.answer(
            text=translator.get(
                key="nickname_setting_message",
                nickname=html.bold(value=message.text)
            ),
            reply_markup=main_keyboard
        )
        return

    post_repository: PostRepository = PostRepository(session=session)
    post = await post_repository.get(post_id=post_id)
    cancel_commenting_keyboard = await get_cancel_commenting_keyboard(translator=translator)

    if not post:
        await message.answer(
            text=translator.get(key="post_not_found_message"),
        )
        return

    comment_id = data.get("comment_id")

    if not comment_id:
        await state.set_state(state=CommentState.COMMENT)
        await message.answer(
            text=translator.get(
                key="send_comment_to_post_message",
                post_link=f'<a href="https://t.me/c/2124435709/{post.id}">'
            ),
            reply_markup=cancel_commenting_keyboard
        )
        return

    comment_repository: CommentRepository = CommentRepository(session=session)
    comment = await comment_repository.get(comment_id=comment_id)

    if not comment:
        await message.answer(
            text=translator.get(key="comment_to_reply_not_found_message"),
        )
        return

    await state.set_state(state=CommentState.REPLY)
    await message.answer(
        text=translator.get(
            key="send_reply_comment_message",
            comment_link=f'<a href="https://t.me/c/2137319935/{comment.message_id}">'
        ),
        reply_markup=cancel_commenting_keyboard
    )
