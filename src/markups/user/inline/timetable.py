from datetime import date

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.factories.timetable import TimetableByDateFactory
from src.translation.translator import LocalizedTranslator


async def get_timetable_dates_menu(
        prev_lessons_date: date,
        next_lessons_date: date,
        date_for_current_timetable: date,
        translator: LocalizedTranslator
) -> InlineKeyboardMarkup:
    """
    Return dates menu for timetable

    :param prev_lessons_date: Previous lessons date
    :param next_lessons_date: Next lessons date
    :param date_for_current_timetable: Selected date
    :param translator: Translator
    """

    timetable_dates_menu = InlineKeyboardBuilder()

    is_prev_date = prev_lessons_date == date_for_current_timetable

    timetable_dates_menu.button(
        text=translator.get(
            key="timetable_list_button_text",
            target_date=prev_lessons_date.strftime("%d.%m.%Y"),
            is_current=is_prev_date
        ),
        callback_data=TimetableByDateFactory(target_date=prev_lessons_date).pack() if not is_prev_date else "timetable"
    )

    timetable_dates_menu.button(
        text=translator.get(
            key="timetable_list_button_text",
            target_date=next_lessons_date.strftime("%d.%m.%Y"),
            is_current=not is_prev_date
        ),
        callback_data=TimetableByDateFactory(target_date=next_lessons_date).pack() if is_prev_date else "timetable"
    )

    return timetable_dates_menu.as_markup()
