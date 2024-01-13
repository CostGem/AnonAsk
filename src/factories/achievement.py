from aiogram.filters.callback_data import CallbackData


class AchievementsFactory(CallbackData, prefix="achievements"):
    pass


class AchievementDetailsFactory(CallbackData, prefix="achievements_details"):
    achievement_id: int
