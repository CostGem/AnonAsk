from aiogram.filters.callback_data import CallbackData


class StatusesFactory(CallbackData, prefix="statuses"):
    pass


class SetStatusFactory(CallbackData, prefix="set_status"):
    status_id: int
