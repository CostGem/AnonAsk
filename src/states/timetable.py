from aiogram.fsm.state import StatesGroup, State


class TimetableState(StatesGroup):
    PHOTO = State()
    DATE = State()
    SCHEDULE = State()
    CONFIRMATION = State()
