from contextlib import suppress

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes.user.user_data import UserData
from src.database.repositories import ScheduleRepository, TimetableRepository, LessonRepository
from src.factories.timetable import TimetableAddDateFactory, TimetableCallScheduleFactory, TimetableAddConfirmFactory, \
    TimetableAddCancelFactory
from src.markups.admin.inline.timetable import get_timetable_dates_for_add_menu, get_schedules_types_menu, \
    get_timetable_add_confirmation_menu
from src.markups.user.reply.main_menu import get_back_to_main_keyboard, get_main_keyboard
from src.states import TimetableState
from src.translation.translator import LocalizedTranslator
from src.utils.admin.lesson import get_lessons_text
from src.utils.admin.sender import send_for_all_users

router = Router(name="Timetable add")


@router.message(Command(commands=["timetable"]), StateFilter(None))
async def add_timetable(message: Message, state: FSMContext, translator: LocalizedTranslator) -> None:
    await state.set_state(state=TimetableState.PHOTO)

    back_to_main_keyboard = await get_back_to_main_keyboard(translator=translator)
    await message.answer(
        text=translator.get(key="send_timetable_photo_message"),
        reply_markup=back_to_main_keyboard
    )


@router.message(F.photo, StateFilter(TimetableState.PHOTO))
async def timetable_photo(message: Message, state: FSMContext, translator: LocalizedTranslator) -> None:
    await state.update_data(timetable_photo=message.photo[-1].file_id)
    await state.set_state(state=TimetableState.DATE)
    timetable_dates_menu = await get_timetable_dates_for_add_menu()
    await message.answer(
        text=translator.get(key="choose_timetable_date_message"),
        reply_markup=timetable_dates_menu
    )


@router.callback_query(TimetableAddDateFactory.filter(), StateFilter(TimetableState.DATE))
async def timetable_add_date(
        call: CallbackQuery,
        callback_data: TimetableAddDateFactory,
        state: FSMContext,
        translator: LocalizedTranslator,
        session: AsyncSession
) -> None:
    with suppress(TelegramBadRequest):
        await call.message.delete()

    timetable_repository: TimetableRepository = TimetableRepository(session=session)
    schedule_repository: ScheduleRepository = ScheduleRepository(session=session)
    timetable_exists = await timetable_repository.exists(timetable_date=callback_data.target_date)
    schedule_types = await schedule_repository.get_all()

    schedule_types_menu = await get_schedules_types_menu(schedule_types=schedule_types)

    await state.update_data(timetable_exists=timetable_exists)
    await state.update_data(timetable_date=f"{callback_data.target_date}")
    await state.set_state(state=TimetableState.SCHEDULE)

    await call.message.answer(
        text=translator.get(key="choose_timetable_schedule_message"),
        reply_markup=schedule_types_menu
    )


@router.callback_query(TimetableCallScheduleFactory.filter(), StateFilter(TimetableState.SCHEDULE))
async def timetable_schedule(
        call: CallbackQuery,
        callback_data: TimetableCallScheduleFactory,
        state: FSMContext,
        translator: LocalizedTranslator,
        session: AsyncSession
) -> None:
    with suppress(TelegramBadRequest):
        await call.message.delete()

    lesson_repository: LessonRepository = LessonRepository(session=session)
    lessons = await lesson_repository.get_all_by_schedule_type(schedule_id=callback_data.schedule_id)
    lessons_text = await get_lessons_text(lessons=lessons)

    data = await state.get_data()
    await state.update_data(schedule_id=callback_data.schedule_id)
    await state.set_state(state=TimetableState.CONFIRMATION)

    timetable_add_confirmation_menu = await get_timetable_add_confirmation_menu(translator=translator)
    await call.message.answer_photo(
        photo=data.get("timetable_photo"),
        caption=translator.get(
            key="timetable_add_confirmation_message",
            target_date=data.get("timetable_date"),
            timetable_exists=data.get("timetable_exists"),
            lessons=lessons_text
        ),
        reply_markup=timetable_add_confirmation_menu
    )


@router.callback_query(TimetableAddConfirmFactory.filter(), StateFilter(TimetableState.CONFIRMATION))
async def confirm_timetable_add(
        call: CallbackQuery,
        state: FSMContext,
        bot: Bot,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    with suppress(TelegramBadRequest):
        await call.message.delete()

    data = await state.get_data()
    await state.clear()

    timetable_repository: TimetableRepository = TimetableRepository(session=session)
    await timetable_repository.create(
        timetable_date=data.get("timetable_date"),
        photo=data.get("timetable_photo"),
        schedule_id=data.get("schedule_id")
    )

    main_keyboard = await get_main_keyboard(translator=translator)
    await call.message.answer(
        text=translator.get(
            key="confirm_timetable_add_message",
            timetable_exists=data.get("timetable_exists"),
            target_date=data.get("timetable_date")
        ),
        reply_markup=main_keyboard
    )

    await send_for_all_users(
        user_repository=user_data.repository,
        bot=bot,
        admin_id=call.from_user.id,
        text=translator.get(
            key="timetable_added_message",
            timetable_exists=data.get("timetable_exists"),
            target_date=data.get("timetable_date")
        ),
        translator=translator
    )


@router.callback_query(TimetableAddCancelFactory.filter(), StateFilter(TimetableState.CONFIRMATION))
async def cancel_timetable_add(call: CallbackQuery, state: FSMContext, translator: LocalizedTranslator) -> None:
    with suppress(TelegramBadRequest):
        await call.message.delete()

    data = await state.get_data()
    await state.clear()

    main_keyboard = await get_main_keyboard(translator=translator)
    await call.message.answer(
        text=translator.get(
            key="cancel_timetable_add_message",
            timetable_exists=data.get("timetable_exists")
        ),
        reply_markup=main_keyboard
    )
