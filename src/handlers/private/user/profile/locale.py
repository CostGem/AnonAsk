from contextlib import suppress

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.classes.user.user_data import UserData
from src.database.repositories import LocaleRepository
from src.factories.locale import ChangeLocaleFactory, SetLocaleFactory
from src.markups.user.inline.locale import get_locales_list_menu
from src.markups.user.reply.main_menu import get_main_keyboard
from src.translation.translator import LocalizedTranslator, TranslatorManager

router = Router(name="Locale")


@router.callback_query(ChangeLocaleFactory.filter())
async def locales_list(
        call: CallbackQuery,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    locale_repository: LocaleRepository = LocaleRepository(session=session)
    locales = await locale_repository.get_all()

    locales_list_menu = await get_locales_list_menu(
        user_data=user_data,
        locales=locales,
        translator=translator
    )

    await call.message.edit_text(
        text=translator.get(key="locales_list_message"),
        reply_markup=locales_list_menu
    )


@router.callback_query(SetLocaleFactory.filter())
async def set_locale(
        call: CallbackQuery,
        callback_data: SetLocaleFactory,
        translator: LocalizedTranslator,
        user_data: UserData,
        session: AsyncSession
) -> None:
    if user_data.locale and user_data.locale.id == callback_data.locale_id:
        await call.answer(
            text=translator.get(key="same_locale_selected_message", emoji=user_data.locale.emoji),
            show_alert=True
        )
        return

    with suppress(TelegramBadRequest):
        await call.message.delete()

    locale_repository: LocaleRepository = LocaleRepository(session=session)

    locale = await locale_repository.get_by_id(locale_id=callback_data.locale_id)
    await locale_repository.update_user_locale(user=user_data.user, locale_id=locale.id)

    translator: LocalizedTranslator = TranslatorManager().get_translator(locale=locale.code)

    main_keyboard = await get_main_keyboard(translator=translator)
    await call.message.answer(
        text=translator.get(key="locale_changed_message", emoji=locale.emoji, name=locale.name),
        reply_markup=main_keyboard
    )
