from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes.user.user_data import UserData
from src.database.repositories import StatusRepository
from src.factories.status import StatusesFactory, SetStatusFactory
from src.markups.user.inline.status import get_statuses_menu
from src.translation.translator import LocalizedTranslator

router = Router(name="Statuses")


@router.callback_query(StatusesFactory.filter(), StateFilter(None))
async def statuses_list(
        call: CallbackQuery,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    status_repository: StatusRepository = StatusRepository(session=session)
    statuses = await status_repository.get_user_statuses(user=user_data.user)

    statuses_menu = await get_statuses_menu(translator=translator, statuses=statuses, user_status=user_data.status)
    await call.message.edit_text(
        text=translator.get(key="user_statuses_message"),
        reply_markup=statuses_menu
    )


@router.callback_query(SetStatusFactory.filter(), StateFilter(None))
async def set_status(
        call: CallbackQuery,
        callback_data: SetStatusFactory,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    if callback_data.status_id == user_data.user.status_id:
        await call.answer()
        return

    status_repository: StatusRepository = StatusRepository(session=session)
    status = await status_repository.get(status_id=callback_data.status_id)

    if not status:
        await call.answer(
            text=translator.get(key="status_not_found_message")
        )

    await status_repository.update_user_status(user=user_data.user, status_id=status.id)

    statuses = await status_repository.get_user_statuses(user=user_data.user)
    user_status = status or user_data.status

    statuses_menu = await get_statuses_menu(translator=translator, statuses=statuses, user_status=user_status)
    await call.message.edit_reply_markup(
        reply_markup=statuses_menu
    )
