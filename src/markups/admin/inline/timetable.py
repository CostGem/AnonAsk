from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import ScheduleTypeModel
from src.factories.timetable import TimetableAddConfirmFactory, TimetableAddCancelFactory, TimetableAddDateFactory, \
    TimetableCallScheduleFactory
from src.translation.translator import LocalizedTranslator
from src.utils.admin.timetable import get_dates_for_timetable


async def get_timetable_add_confirmation_menu(translator: LocalizedTranslator) -> InlineKeyboardMarkup:
    """
    Return timetable add confirmation menu

    :param translator: Translator
    """

    timetable_add_confirmation_menu = InlineKeyboardBuilder()

    timetable_add_confirmation_menu.button(
        text=translator.get(key="confirm_timetable_add_button_text"),
        callback_data=TimetableAddConfirmFactory().pack()
    )

    timetable_add_confirmation_menu.button(
        text=translator.get(key="cancel_timetable_add_button_text"),
        callback_data=TimetableAddCancelFactory().pack()
    )

    return timetable_add_confirmation_menu.adjust(1).as_markup()


async def get_timetable_dates_for_add_menu() -> InlineKeyboardMarkup:
    """
    Return a list of dates for add timetable
    """

    prev_lessons_date, next_lessons_date, date_for_current_timetable = await get_dates_for_timetable()
    timetable_dates_menu = InlineKeyboardBuilder()

    timetable_dates_menu.button(
        text=prev_lessons_date.strftime("%d.%m.%Y"),
        callback_data=TimetableAddDateFactory(target_date=prev_lessons_date).pack()
    )

    timetable_dates_menu.button(
        text=next_lessons_date.strftime("%d.%m.%Y"),
        callback_data=TimetableAddDateFactory(target_date=next_lessons_date).pack()
    )

    return timetable_dates_menu.as_markup()


async def get_schedules_types_menu(schedule_types: List[ScheduleTypeModel]) -> InlineKeyboardMarkup:
    """
    Return schedules types menu

    :param schedule_types: List of schedules types
    """

    schedule_types_menu = InlineKeyboardBuilder()

    for schedule in schedule_types:
        schedule_types_menu.button(
            text=schedule.name,
            callback_data=TimetableCallScheduleFactory(schedule_id=schedule.id).pack()
        )

    return schedule_types_menu.adjust(1).as_markup()
