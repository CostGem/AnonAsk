from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand, BotCommandScopeChat

from src.enums import Role
from src.translation.translator import LocalizedTranslator
from src.markups.user.inline.register import get_nickname_set_menu
from src.markups.user.reply.comment import get_cancel_commenting_keyboard
from src.markups.user.reply.main_menu import get_main_keyboard

from src.classes.user.user_data import UserData
from src.states import CommentState

router = Router(name="Start command")


# @router.message(
#     CommandStart(deep_link=True, magic=F.args.startswith("achievement_")),
# )
# async def start_achievement(
#         message: Message,
#         command: CommandObject,
#         state: FSMContext,
#         translator: LocalizedTranslator,
#         user_data: UserData,
#         bot: Bot
# ) -> None:
#     achievement_code = command.args[12:]
#     if user_data.user:
#         achievement_property = await crud.achievement.get_achievement_properties_by_code(code=achievement_code)
#
#         if not achievement_property:
#             await message.answer(
#                 text=translator.get(key="achievement_property_not_found_message"),
#             )
#             return
#
#         achievement = await achievement_property.achievement.get()
#
#         if await crud.achievement.user_have_achievement(user=user_data.user, achievement=achievement):
#             await message.answer(
#                 text=translator.get(key="user_have_achievement_message")
#             )
#             return
#
#         if await crud.achievement.user_activated_achievement(
#                 user=user_data.user,
#                 achievement_property=achievement_property
#         ):
#             await message.answer(
#                 text=translator.get(key="user_activated_achievement_message")
#             )
#             return
#
#         if achievement_property.from_date and achievement_property.from_date > datetime.utcnow():
#             await message.answer(
#                 text=translator.get(key="achievement_activation_from_date_message")
#             )
#             return
#
#         if achievement_property.until_date and achievement_property.until_date < datetime.utcnow():
#             await message.answer(
#                 text=translator.get(key="achievement_activation_until_date_message")
#             )
#             return
#
#         status = await achievement.award_status.get()
#
#         await crud.achievement.activate_achievement(
#             user=user_data.user,
#             achievement=achievement,
#             achievement_property=achievement_property,
#             status=status
#         )
#
#         main_keyboard = await get_main_keyboard(translator=translator)
#
#         await message.answer(
#             text=translator.get(
#                 key="achievement_activated_success_message",
#                 achievement_name=achievement.name,
#                 status_emoji=status.emoji
#             ),
#             reply_markup=main_keyboard
#         )
#     else:
#         await state.update_data(achievement_code=achievement_code)
#         nickname_set_menu = await get_nickname_set_menu(translator=translator)
#         await message.answer(
#             text=translator.get(key="welcome_message"),
#             reply_markup=nickname_set_menu
#         )
#
#     if user_data.role and user_data.role.level == UserRoles.ADMIN:
#         await bot.set_my_commands(
#             commands=[
#                 BotCommand(
#                     command="start",
#                     description=translator.get(key="start_command_description")
#                 ),
#                 BotCommand(
#                     command="timetable",
#                     description=translator.get(key="timetable_command_description")
#                 )
#             ],
#             scope=BotCommandScopeChat(type="chat", chat_id=message.from_user.id),
#             language_code=translator.locale
#         )
#     else:
#         await bot.set_my_commands(
#             commands=[
#                 BotCommand(
#                     command="start",
#                     description=translator.get(key="start_command_description")
#                 )
#             ],
#             scope=BotCommandScopeChat(type="chat", chat_id=message.from_user.id),
#             language_code=translator.locale
#         )


# @router.message(
#     CommandStart(deep_link=True, magic=F.args.startswith("comment_")),
# )
# async def start_commenting(
#         message: Message,
#         command: CommandObject,
#         state: FSMContext,
#         translator: LocalizedTranslator,
#         user_data: UserData
# ) -> None:
#     args = list(map(int, command.args[8:].split("_")))
#     await state.update_data(post_id=args[0])
#     if post := await crud.post.get_post_by_id(post_id=args[0]):
#         cancel_commenting_keyboard = await get_cancel_commenting_keyboard(translator=translator)
#         if len(args) == 2:
#             await state.update_data(comment_id=args[1])
#             if comment := await crud.comment.get_comment_by_id(comment_id=args[1]):
#                 if user_data.user:
#                     await state.set_state(state=CommentState.REPLY)
#                     await message.answer(
#                         text=translator.get(
#                             key="send_reply_comment_message",
#                             comment_link=f'<a href="https://t.me/c/2137319935/{comment.message_id}">'
#                         ),
#                         reply_markup=cancel_commenting_keyboard
#                     )
#                 else:
#                     nickname_set_menu = await get_nickname_set_menu(translator=translator)
#                     await message.answer(
#                         text=translator.get(key="welcome_message"),
#                         reply_markup=nickname_set_menu
#                     )
#             else:
#                 await message.answer(
#                     text=translator.get(key="comment_to_reply_not_found_message"),
#                 )
#         else:
#             if user_data.user:
#                 await state.set_state(state=CommentState.COMMENT)
#                 await message.answer(
#                     text=translator.get(
#                         key="send_comment_to_post_message",
#                         post_link=f'<a href="https://t.me/c/2124435709/{post.id}">'
#                     ),
#                     reply_markup=cancel_commenting_keyboard
#                 )
#             else:
#                 nickname_set_menu = await get_nickname_set_menu(translator=translator)
#                 await message.answer(
#                     text=translator.get(key="welcome_message"),
#                     reply_markup=nickname_set_menu
#                 )
#     else:
#         await message.answer(
#             text=translator.get(key="post_not_found_message"),
#         )


@router.message(CommandStart())
async def start_command(
        message: Message,
        translator: LocalizedTranslator,
        user_data: UserData,
        state: FSMContext,
        bot: Bot
) -> None:
    await state.clear()
    if user_data.role and user_data.role.level == Role.ADMIN:
        await bot.set_my_commands(
            commands=[
                BotCommand(
                    command="start",
                    description=translator.get(key="start_command_description")
                ),
                BotCommand(
                    command="timetable",
                    description=translator.get(key="timetable_command_description")
                )
            ],
            scope=BotCommandScopeChat(type="chat", chat_id=message.from_user.id),
            language_code=translator.locale
        )
    else:
        await bot.set_my_commands(
            commands=[
                BotCommand(
                    command="start",
                    description=translator.get(key="start_command_description")
                )
            ],
            scope=BotCommandScopeChat(type="chat", chat_id=message.from_user.id),
            language_code=translator.locale
        )

    main_keyboard = await get_main_keyboard(translator=translator)
    await message.answer(
        text=translator.get(key="welcome_message"),
        reply_markup=main_keyboard
    )
