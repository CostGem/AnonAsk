from aiogram.fsm.state import StatesGroup, State


class NicknameState(StatesGroup):
    NICKNAME = State()
