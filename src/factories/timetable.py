from datetime import date

from aiogram.filters.callback_data import CallbackData


class TimetableByDateFactory(CallbackData, prefix="timetable_by_date"):
    target_date: date


class TimetableAddDateFactory(CallbackData, prefix="timetable_add_date"):
    target_date: date


class TimetableAddConfirmFactory(CallbackData, prefix="timetable_add_confirm"):
    pass


class TimetableAddCancelFactory(CallbackData, prefix="timetable_add_cancel"):
    pass


class TimetableCallScheduleFactory(CallbackData, prefix="timetable_schedule"):
    schedule_id: int
