from aiogram.fsm.state import StatesGroup, State


class ScheduleCreationState(StatesGroup):
    PHOTO = State()
    SCHEDULE_TYPE = State()
    CONFIRMATION = State()
    NOTIFICATION = State()
