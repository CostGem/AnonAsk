from aiogram.fsm.state import StatesGroup, State


class AnonimMessageState(StatesGroup):
    MESSAGE: State = State()
