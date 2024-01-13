from aiogram.fsm.state import StatesGroup, State


class CommentState(StatesGroup):
    COMMENT = State()
    REPLY = State()
