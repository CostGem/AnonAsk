from aiogram.filters.callback_data import CallbackData


class ChangeLocaleFactory(CallbackData, prefix="change_locale"):
    pass


class SetLocaleFactory(CallbackData, prefix="set_locale"):
    locale_id: int
