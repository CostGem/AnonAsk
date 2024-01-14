# from datetime import datetime
#
# from aiogram import Router, html
# from aiogram.types import Message
# from aiogram.filters import Command
#
# from database import crud
# from locales.translator import LocalizedTranslator
# from utils.timetable import get_dates_for_timetable
#
# router = Router(name="Lesson time")
#
#
# @router.message(Command(commands="lesson"))
# async def lesson_time(message: Message, translator: LocalizedTranslator) -> None:
#     current_time = datetime(year=2024, month=1, day=9, hour=10, minute=5)
#     timetable = await crud.timetable.get_timetable_by_date(target_date=current_time.date())
#     if timetable:
#         schedule = await timetable.schedule.get()
#         last_lesson = await crud.lesson.get_last_lesson(schedule_id=schedule.pk)
#         await message.answer(
#             text=f"{current_time.time()}"
#         )
#         if lesson := await crud.lesson.get_lesson_by_time(current_time=current_time.time(), schedule_id=schedule.pk):
#             time_to_lesson_left = lesson.end_at - current_time.time()
#             await message.answer(
#                 text=f"{time_to_lesson_left}"
#             )
#         else:
#             await message.answer(
#                 text=translator.get(key="no_more_lessons_message")
#             )
#     else:
#         await message.answer(
#             text=translator.get(key="today_timetable_not_found_message")
#         )
