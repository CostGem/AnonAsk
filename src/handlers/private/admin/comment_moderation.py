from contextlib import suppress

from aiogram import Router, F, html, Bot
from aiogram.enums import MessageEntityType
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes.user.user_data import UserData
from src.database.repositories import PostRepository, CommentRepository, RoleRepository, StatusRepository
from src.enums import Role
from src.factories.comment_moderation import CommentDeleteFactory, CommentUserBanFactory
from src.markups.admin.inline.comment_moderation import get_comment_moderation_menu
from src.translation.translator import LocalizedTranslator
from src.utils.admin.comment import delete_comments

router = Router(name="Comments moderation")


@router.message(F.forward_from.id == F.bot.id)
async def comment_info(
        message: Message,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    data = {}

    if message.entities:
        for entity in message.entities:
            if entity.type in (MessageEntityType.TEXT_LINK, MessageEntityType.URL, MessageEntityType):
                data["url"] = entity.url

    commenting_url = data.get("url")

    if not commenting_url:
        await message.answer(
            text=translator.get(key="its_not_comment_message")
        )
        return

    post_id, comment_id = tuple(map(int, commenting_url[42:].split("_")))

    post_repository: PostRepository = PostRepository(session=session)
    comment_repository: CommentRepository = CommentRepository(session=session)
    role_repository: RoleRepository = RoleRepository(session=session)
    status_repository: StatusRepository = StatusRepository(session=session)

    post = await post_repository.get(post_id=post_id)
    comment = await comment_repository.get(comment_id=comment_id)

    if not post or not comment:
        await message.answer(
            text=translator.get(key="comment_not_found_message")
        )
        return

    user = await user_data.repository.get_by_pk(user_id=comment.user_id)
    user_role = await role_repository.get(role_id=user.role_id)
    user_status = await status_repository.get(status_id=user.status_id)

    comment_moderation_menu = await get_comment_moderation_menu(comment_id=comment.id, translator=translator)
    await message.reply(
        text=translator.get(
            key="comment_user_info_message",
            nickname=html.bold(value=user.nickname),
            name=html.link(value=user.name, link=f"tg://user?id={user.user_id}"),
            have_username=bool(user.username),
            username=user.username,
            status_emoji=user_status.emoji,
            role_name=user_role.name
        ),
        reply_markup=comment_moderation_menu
    )


@router.callback_query(CommentDeleteFactory.filter())
async def comment_delete(
        call: CallbackQuery,
        callback_data: CommentDeleteFactory,
        bot: Bot,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    with suppress(TelegramBadRequest):
        await call.message.delete()

    comment_repository: CommentRepository = CommentRepository(session=session)
    comment = await comment_repository.get(comment_id=callback_data.comment_id)

    if not comment:
        await call.answer(
            text=translator.get(key="comment_not_found_message"),
            show_alert=True
        )
        return

    role_repository: RoleRepository = RoleRepository(session=session)
    user = await user_data.repository.get_by_pk(user_id=comment.user_id)
    user_role = await role_repository.get(role_id=user.role_id)

    if user_role.level == Role.ADMIN or user.user_id == call.from_user.id:
        await call.message.answer(
            text=translator.get(key="you_can_not_delete_an_admin_message")
        )
        return

    await delete_comments(comment=comment, comment_repository=comment_repository, bot=bot)
    await call.message.answer(
        text=translator.get(
            key="comments_deleted_message",
            comment_id=comment.id
        )
    )
    if not user.is_chat_blocked and not user.is_banned:
        await call.bot.send_message(
            chat_id=user.user_id,
            text=translator.get(
                key="your_comment_has_been_deleted_message",
                comment_id=comment.id
            ),
            disable_web_page_preview=True
        )


@router.callback_query(CommentUserBanFactory.filter())
async def comment_user_ban(
        call: CallbackQuery,
        callback_data: CommentUserBanFactory,
        bot: Bot,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    with suppress(TelegramBadRequest):
        await call.message.delete()

    comment_repository: CommentRepository = CommentRepository(session=session)
    comment = await comment_repository.get(comment_id=callback_data.comment_id)

    if not comment:
        await call.answer(
            text=translator.get(key="comment_not_found_message"),
            show_alert=True
        )
        return

    role_repository: RoleRepository = RoleRepository(session=session)
    user = await user_data.repository.get_by_pk(user_id=comment.user_id)
    user_role = await role_repository.get(role_id=user.role_id)

    if user_role.level == Role.ADMIN or user.user_id == call.from_user.id:
        await call.message.answer(
            text=translator.get(key="you_can_not_delete_an_admin_message")
        )
        return

    await user_data.repository.ban(user=user)

    await delete_comments(comment=comment, comment_repository=comment_repository, bot=bot)
    await call.message.answer(
        text=translator.get(
            key="comments_deleted_and_user_banned_message",
            comment_id=comment.id
        )
    )
    if not user.is_chat_blocked and not user.is_banned:
        await call.bot.send_message(
            chat_id=user.user_id,
            text=translator.get(
                key="you_have_been_blocked",
                comment_id=comment.id
            ),
            disable_web_page_preview=True
        )
