from typing import Optional

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes.types.album import Album
from src.config import CONFIGURATION
from src.database.repositories import PostRepository
from src.filters import PostMessageFilter
from src.translation.translator import LocalizedTranslator

router = Router(name="Editing chanel post")


@router.channel_post(F.chat.id == CONFIGURATION.DATA.channel_id, ~F.poll)
async def handle_channel_post(post: Message, general_translator: LocalizedTranslator, session: AsyncSession):
    is_commentable = not post.html_text.endswith("$")
    post_repository: PostRepository = PostRepository(session=session)
    channel_post = await post_repository.create(post_id=post.message_id, is_commentable=is_commentable)

    if not is_commentable:
        post_message = general_translator.get(
            key="post_message",
            have_text=bool(post.html_text),
            post_text=post.html_text,
            comment_post_url=f'<a href="https://t.me/news_sosh1_bot?start=comment_{channel_post.id}">'
        )
    else:
        post_message = post.html_text[:-1]

    if post.text:
        if post_message != "":
            await post.edit_text(
                text=post_message,
                disable_web_page_preview=True
            )
        else:
            await post.delete()
    else:
        await post.edit_caption(
            caption=post_message if post_message != "" else None
        )


@router.message(StateFilter(None), PostMessageFilter())
async def handle_forwarded_post(message: Message, session: AsyncSession, album: Optional[Album] = None) -> None:
    post_id = album.messages[0].forward_from_message_id if album else message.forward_from_message_id
    post_repository: PostRepository = PostRepository(session=session)
    post = await post_repository.get(post_id=post_id)

    if post:
        if not post.is_commentable:
            await message.delete()
        else:
            await post_repository.update_post_message_id_in_chat(post_id=post_id, post_message_id=message.message_id)
