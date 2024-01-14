from aiogram import Router, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes.user.user_data import UserData
from src.config import CONFIGURATION
from src.database.repositories import PostRepository, CommentRepository
from src.filters import KeyboardButtonFilter, CommentFilter
from src.markups.user.reply.main_menu import get_main_keyboard
from src.states import CommentState
from src.translation.translator import LocalizedTranslator
from src.utils.admin import sender

router = Router(name="Post commenting")


@router.message(KeyboardButtonFilter(key="cancel_commenting_button_text"), StateFilter(CommentState))
async def cancel_commenting(message: Message, state: FSMContext, translator: LocalizedTranslator) -> None:
    await state.clear()

    main_keyboard = await get_main_keyboard(translator=translator)
    await message.answer(
        text=translator.get(key="cancel_commenting_message"),
        reply_markup=main_keyboard
    )


@router.message(StateFilter(CommentState.COMMENT), CommentFilter())
async def comment_to_post(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    data = await state.get_data()
    await state.clear()

    post_repository: PostRepository = PostRepository(session=session)
    post = await post_repository.get(post_id=data.get("post_id"))

    if not post:
        await message.answer(
            text=translator.get(key="post_not_found_message")
        )
        return

    comment_repository: CommentRepository = CommentRepository(session=session)
    comment = await comment_repository.create(post=post, user=user_data.user)
    main_keyboard = await get_main_keyboard(translator=translator)

    comment_message = translator.get(
        key="comment_message",
        status_emoji=user_data.status.emoji,
        nickname=user_data.user.nickname,
        have_text=bool(message.html_text),
        user_message=html.italic(value=message.html_text),
        reply_to_comment_url=f'<a href="https://t.me/news_sosh1_bot?start=comment_{post.id}_{comment.id}">'
    )

    comment_message_id = await sender.send_message(
        bot=message.bot,
        chat_id=CONFIGURATION.DATA.comment_chat_id,
        text=comment_message,
        photo=message.photo,
        video=message.video,
        sticker=message.sticker,
        reply_message_id=post.post_id_in_chat
    )

    await comment_repository.update_comment_message_id(comment=comment, message_id=comment_message_id)

    await message.answer(
        text=translator.get(
            key="comment_sent_successfully_message",
            post_url=f'<a href="https://t.me/c/2124435709/{post.id}">',
            comment_url=f"https://t.me/c/2137319935/{comment_message_id}"
        ),
        reply_markup=main_keyboard
    )


@router.message(StateFilter(CommentState.REPLY), CommentFilter())
async def reply_to_comment(
        message: Message,
        state: FSMContext,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    data = await state.get_data()
    await state.clear()

    post_repository: PostRepository = PostRepository(session=session)
    post = await post_repository.get(post_id=data.get("post_id"))

    if not post:
        await message.answer(
            text=translator.get(key="post_not_found_message")
        )
        return

    comment_repository: CommentRepository = CommentRepository(session=session)
    reply_comment = await comment_repository.get(comment_id=data.get("comment_id"))

    if not reply_comment:
        await message.answer(
            text=translator.get(key="comment_to_reply_not_found_message")
        )
        return

    if reply_comment.parent_comment_id:
        parent_comment = await comment_repository.get(comment_id=reply_comment.parent_comment_id)
        parent_comment_id = parent_comment.id
    else:
        parent_comment_id = reply_comment.id

    comment = await comment_repository.create(post=post, user=user_data.user, parent_comment_id=parent_comment_id)
    reply_comment_user = await user_data.repository.get_by_pk(user_id=reply_comment.user_id)

    comment_message = translator.get(
        key="comment_message",
        status_emoji=user_data.status.emoji,
        nickname=user_data.user.nickname,
        have_text=bool(message.html_text),
        user_message=html.italic(value=message.html_text),
        reply_to_comment_url=f'<a href="https://t.me/news_sosh1_bot?start=comment_{post.id}_{comment.id}">'
    )

    comment_message_id = await sender.send_message(
        bot=message.bot,
        chat_id=CONFIGURATION.DATA.comment_chat_id,
        text=comment_message,
        photo=message.photo,
        video=message.video,
        sticker=message.sticker,
        reply_message_id=reply_comment.message_id
    )

    await comment_repository.update_comment_message_id(comment=comment, message_id=comment_message_id)

    main_keyboard = await get_main_keyboard(translator=translator)
    await message.answer(
        text=translator.get(
            key="reply_to_comment_sent_successfully_message",
            comment_url=f'<a href="https://t.me/c/2137319935/{reply_comment.message_id}">',
            reply_url=f"https://t.me/c/2137319935/{comment_message_id}"
        ),
        reply_markup=main_keyboard
    )

    if not reply_comment_user.is_chat_blocked and reply_comment_user.is_banned:
        await message.bot.send_message(
            chat_id=reply_comment_user.user_id,
            text=translator.get(
                key="user_reply_to_our_comment_message",
                nickname=html.bold(value=user_data.user.nickname),
                reply_url=f'<a href="https://t.me/c/2137319935/{comment_message_id}">',
                comment_url=f'<a href="https://t.me/c/2137319935/{reply_comment.message_id}">'
            )
        )
