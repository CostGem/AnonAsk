from datetime import date, datetime, timedelta


async def get_dates_for_timetable() -> (date, date, date):
    """
    Return dates for timetable
    """

    current_time = datetime.utcnow()
    current_date = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    weekday = current_date.isoweekday()

    if weekday in (5, 6, 7):
        days_for_next_lessons_day = 8 - weekday
        days_for_prev_lessons_day = weekday - 5 if weekday in (6, 7) else 0
    else:
        days_for_next_lessons_day = 1
        days_for_prev_lessons_day = 0

    prev_lessons_date = current_date - timedelta(days=days_for_prev_lessons_day)
    next_lessons_date = current_date + timedelta(days=days_for_next_lessons_day)
    rescheduling_time = current_date.replace(hour=10, minute=0, second=0, microsecond=0)

    if current_time >= rescheduling_time or weekday in (6, 7):
        return prev_lessons_date.date(), next_lessons_date.date(), next_lessons_date.date()
    else:
        return prev_lessons_date.date(), next_lessons_date.date(), prev_lessons_date.date()
