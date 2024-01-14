from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes.user.user_data import UserData
from src.database.repositories import PostRepository, CommentRepository, AchievementRepository, StatusRepository
from src.markups.user.inline.register import get_nickname_set_menu
from src.markups.user.reply.comment import get_cancel_commenting_keyboard
from src.markups.user.reply.main_menu import get_main_keyboard
from src.states import CommentState
from src.translation.translator import LocalizedTranslator
from src.utils.service.bot_comands import set_bot_commands

router = Router(name="Start command")


@router.message(
    CommandStart(deep_link=True, magic=F.args.startswith("achievement_")),
)
async def start_achievement(
        message: Message,
        command: CommandObject,
        bot: Bot,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    user_data.user = await user_data.repository.register(
        user_id=message.from_user.id,
        name=message.from_user.full_name,
        username=message.from_user.username
    )

    await set_bot_commands(user_data=user_data, bot=bot, translator=translator)

    achievement_code = command.args[12:]
    achievement_repository: AchievementRepository = AchievementRepository(session=session)
    achievement_activation_code = await achievement_repository.get_achievement_activation_code(code=achievement_code)

    if not achievement_activation_code:
        await message.answer(
            text=translator.get(key="achievement_property_not_found_message"),
        )
        return

    achievement = await achievement_repository.get(achievement_id=achievement_activation_code.achievement_id)

    if await achievement_repository.user_has_achievement(user=user_data.user, achievement_id=achievement.id):
        await message.answer(
            text=translator.get(key="user_have_achievement_message")
        )
        return

    if await achievement_repository.user_activated_achievement(
            user_id=user_data.user.id,
            activation_code_id=achievement_activation_code.id
    ):
        await message.answer(
            text=translator.get(key="user_activated_achievement_message")
        )
        return

    if achievement_activation_code.from_date and achievement_activation_code.from_date > datetime.utcnow():
        await message.answer(
            text=translator.get(key="achievement_activation_from_date_message")
        )
        return

    if achievement_activation_code.until_date and achievement_activation_code.until_date < datetime.utcnow():
        await message.answer(
            text=translator.get(key="achievement_activation_until_date_message")
        )
        return

    status_repository: StatusRepository = StatusRepository(session=session)
    status = await status_repository.get(status_id=achievement.award_status_id)

    user_has_status = await status_repository.user_has_status(user_id=user_data.user.id, status_id=status.id)

    await achievement_repository.activate_achievement(
        user=user_data.user,
        achievement=achievement,
        achievement_activation_code=achievement_activation_code,
        user_has_status=user_has_status,
        status=status
    )

    main_keyboard = await get_main_keyboard(translator=translator)
    await message.answer(
        text=translator.get(
            key="achievement_activated_success_message",
            achievement_name=achievement.name,
            status_emoji=status.emoji
        ),
        reply_markup=main_keyboard
    )


@router.message(CommandStart(deep_link=True, magic=F.args.startswith("comment_")))
async def start_commenting(
        message: Message,
        command: CommandObject,
        state: FSMContext,
        bot: Bot,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    user_data.user = await user_data.repository.register(
        user_id=message.from_user.id,
        name=message.from_user.full_name,
        username=message.from_user.username
    )

    await set_bot_commands(user_data=user_data, bot=bot, translator=translator)

    args = list(map(int, command.args[8:].split("_")))
    post_id = args[0]
    await state.update_data(post_id=args[0])

    post_repository: PostRepository = PostRepository(session=session)

    post = await post_repository.get(post_id=post_id)

    if not post:
        await message.answer(
            text=translator.get(key="post_not_found_message"),
        )
        return

    if not user_data.user.nickname:
        await state.clear()
        nickname_set_menu = await get_nickname_set_menu(translator=translator)
        await message.answer(
            text=translator.get(key="nickname_not_set_message"),
            reply_markup=nickname_set_menu
        )
        return

    cancel_commenting_keyboard = await get_cancel_commenting_keyboard(translator=translator)

    if len(args) == 2:
        comment_id = args[1]
        await state.update_data(comment_id=comment_id)

        comment_repository: CommentRepository = CommentRepository(session=session)
        comment = await comment_repository.get(comment_id=comment_id)

        if not comment:
            await message.answer(
                text=translator.get(key="comment_to_reply_not_found_message"),
            )

        await state.set_state(state=CommentState.REPLY)
        await message.answer(
            text=translator.get(
                key="send_reply_comment_message",
                comment_link=f'<a href="https://t.me/c/2137319935/{comment.message_id}">'
            ),
            reply_markup=cancel_commenting_keyboard
        )
    else:
        await state.set_state(state=CommentState.COMMENT)
        await message.answer(
            text=translator.get(
                key="send_comment_to_post_message",
                post_link=f'<a href="https://t.me/c/2124435709/{post.id}">'
            ),
            reply_markup=cancel_commenting_keyboard
        )


@router.message(CommandStart())
async def start_command(
        message: Message,
        bot: Bot,
        translator: LocalizedTranslator,
        user_data: UserData,
        state: FSMContext
) -> None:
    await state.clear()

    user_data.user = await user_data.repository.register(
        user_id=message.from_user.id,
        name=message.from_user.full_name,
        username=message.from_user.username
    )

    await set_bot_commands(user_data=user_data, bot=bot, translator=translator)

    main_keyboard = await get_main_keyboard(translator=translator)
    await message.answer(
        text=translator.get(key="welcome_message"),
        reply_markup=main_keyboard
    )
