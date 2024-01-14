from contextlib import suppress

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories import TimetableRepository, LessonRepository
from src.factories.timetable import TimetableByDateFactory
from src.filters import KeyboardButtonFilter
from src.markups.user.inline.timetable import get_timetable_dates_menu
from src.translation.translator import LocalizedTranslator
from src.utils.admin.lesson import get_lessons_text
from src.utils.admin.timetable import get_dates_for_timetable

router = Router(name="Timetable")


@router.message(KeyboardButtonFilter(key="timetable_button_text"))
async def current_timetable(message: Message, translator: LocalizedTranslator, session: AsyncSession) -> None:
    prev_lessons_date, next_lessons_date, date_for_current_timetable = await get_dates_for_timetable()
    timetable_repository: TimetableRepository = TimetableRepository(session=session)
    timetable = await timetable_repository.get_by_date(timetable_date=date_for_current_timetable)
    timetable_dates_menu = await get_timetable_dates_menu(
        prev_lessons_date=prev_lessons_date,
        next_lessons_date=next_lessons_date,
        date_for_current_timetable=date_for_current_timetable,
        translator=translator
    )

    if not timetable:
        await message.answer(
            text=translator.get(
                key="timetable_not_found",
                is_today_selected=date_for_current_timetable == prev_lessons_date,
                today_date=prev_lessons_date,
                tomorrow_date=next_lessons_date
            ),
            reply_markup=timetable_dates_menu
        )
        return

    lesson_repository: LessonRepository = LessonRepository(session=session)
    lessons = await lesson_repository.get_all_by_schedule_type(schedule_id=timetable.schedule_id)
    lessons_text = await get_lessons_text(lessons=lessons)

    await message.answer_photo(
        photo=timetable.photo,
        caption=translator.get(
            key="timetable_message",
            prev_lessons_date=prev_lessons_date,
            next_lessons_date=next_lessons_date,
            is_today_timetable=date_for_current_timetable == prev_lessons_date,
            lessons=lessons_text
        ),
        reply_markup=timetable_dates_menu
    )


@router.callback_query(TimetableByDateFactory.filter(), StateFilter(None))
async def timetable_by_date(
        call: CallbackQuery,
        callback_data: TimetableByDateFactory,
        translator: LocalizedTranslator,
        session: AsyncSession
) -> None:
    timetable_repository: TimetableRepository = TimetableRepository(session=session)
    prev_lessons_date, next_lessons_date, date_for_current_timetable = await get_dates_for_timetable()
    date_for_current_timetable = callback_data.target_date

    timetable = await timetable_repository.get_by_date(timetable_date=date_for_current_timetable)
    timetable_dates_menu = await get_timetable_dates_menu(
        prev_lessons_date=prev_lessons_date,
        next_lessons_date=next_lessons_date,
        date_for_current_timetable=date_for_current_timetable,
        translator=translator
    )

    if not timetable:
        await call.answer(
            text=translator.get(
                key="timetable_not_found",
                is_today_selected=date_for_current_timetable == prev_lessons_date,
                today_date=prev_lessons_date,
                tomorrow_date=next_lessons_date
            ),
            show_alert=True
        )
        return

    with suppress(TelegramBadRequest):
        await call.message.delete()

    lesson_repository: LessonRepository = LessonRepository(session=session)
    lessons = await lesson_repository.get_all_by_schedule_type(schedule_id=timetable.schedule_id)
    lessons_text = await get_lessons_text(lessons=lessons)

    await call.message.answer_photo(
        photo=timetable.photo,
        caption=translator.get(
            key="timetable_message",
            prev_lessons_date=prev_lessons_date,
            next_lessons_date=next_lessons_date,
            is_today_timetable=date_for_current_timetable == prev_lessons_date,
            lessons=lessons_text
        ),
        reply_markup=timetable_dates_menu
    )
