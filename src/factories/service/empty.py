from aiogram.filters.callback_data import CallbackData


class EmptyFactory(CallbackData, prefix="empty"):
    pass
