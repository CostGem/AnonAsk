from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.user.achievement import get_achievements_text

from src.classes.user.user_data import UserData
from src.database.repositories import AchievementRepository, StatusRepository
from src.factories.achievement import AchievementsFactory, AchievementDetailsFactory
from src.markups.user.inline.achievement import get_to_achievements_menu, get_achievements_menu
from src.markups.user.inline.profile import get_to_profile_menu
from src.translation.translator import LocalizedTranslator

router = Router(name="Achievements")


@router.callback_query(AchievementsFactory.filter(), StateFilter(None))
async def user_achievements(
        call: CallbackQuery,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    achievement_repository: AchievementRepository = AchievementRepository(session=session)
    achievements = await achievement_repository.get_user_achievements(user=user_data.user)

    if len(achievements) > 0:
        achievements_menu = await get_achievements_menu(achievements=achievements, translator=translator)
        achievements_text = await get_achievements_text(achievements=achievements, translator=translator)
        await call.message.edit_text(
            text=achievements_text,
            reply_markup=achievements_menu
        )
    else:
        to_profile_menu = await get_to_profile_menu(translator=translator)
        await call.message.edit_text(
            text=translator.get(key="you_have_not_achievements_message"),
            reply_markup=to_profile_menu
        )


@router.callback_query(AchievementDetailsFactory.filter(), StateFilter(None))
async def achievement_details(
        call: CallbackQuery,
        callback_data: AchievementDetailsFactory,
        translator: LocalizedTranslator,
        session: AsyncSession
) -> None:
    achievement_repository: AchievementRepository = AchievementRepository(session=session)
    status_repository: StatusRepository = StatusRepository(session=session)
    achievement = await achievement_repository.get(achievement_id=callback_data.achievement_id)

    if achievement:
        status = await status_repository.get(status_id=achievement.award_status_id)
        to_achievements_menu = await get_to_achievements_menu(translator=translator)
        await call.message.edit_text(
            text=translator.get(
                key="achievement_details_message",
                achievement_name=achievement.name,
                achievement_description=achievement.description,
                status_emoji=status.emoji
            ),
            reply_markup=to_achievements_menu
        )
