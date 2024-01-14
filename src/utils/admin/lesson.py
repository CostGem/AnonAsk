from typing import List

from src.database.models import LessonModel


async def get_lessons_text(lessons: List[LessonModel]) -> str:
    """
    Return text of lessons schedule

    :param lessons: List of lessons
    """

    lessons_text: str = ""

    for lesson in lessons:
        start_at = lesson.start_at.strftime("%H:%M")
        end_at = lesson.end_at.strftime("%H:%M")
        lessons_text += f"{lesson.number} урок - {start_at}-{end_at}\n"

    return lessons_text
