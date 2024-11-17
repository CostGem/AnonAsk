import logging

from aiogram import Bot
from aiogram import Dispatcher
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector.wiring import inject, Provide

from src.config import CONFIGURATION
from src.containers.app import AppContainer
from src.handlers import router
from src.middlewares import (
    ThrottlingMiddleware,
    DatabaseMiddleware,
    UserAccountMiddleware,
    TranslatorMiddleware
)
from src.utils.service.logger import configure_logging


@inject
def set_dispatcher_injections(dp: Dispatcher = Provide[AppContainer.dp]) -> None:
    """
    Create and configures a dispatcher for handling requests, using a Redis storage backend

    :param dp: Dispatcher
    """

    scheduler: AsyncIOScheduler = get_scheduler()

    dp["scheduler"] = scheduler

    dp.include_router(router=router)


@inject
def get_scheduler(scheduler: AsyncIOScheduler = Provide[AppContainer.scheduler]) -> AsyncIOScheduler:
    """Returns a scheduler"""

    scheduler.add_executor(executor=AsyncIOExecutor())

    scheduler.add_jobstore(
        jobstore=RedisJobStore(
            username=CONFIGURATION.REDIS.USER,
            password=CONFIGURATION.REDIS.PASSWORD,
            host=CONFIGURATION.REDIS.HOST,
            port=CONFIGURATION.REDIS.PORT,
        )
    )

    logging.getLogger("apscheduler").setLevel(logging.ERROR)

    return scheduler


@inject
def register_middlewares(dp: Dispatcher = Provide[AppContainer.dp]) -> None:
    """
    Registers middlewares

    :param dp: Dispatcher
    """

    # Throttling
    dp.message.outer_middleware(ThrottlingMiddleware())
    dp.callback_query.outer_middleware(ThrottlingMiddleware())

    # Database
    dp.message.outer_middleware(DatabaseMiddleware())
    dp.callback_query.outer_middleware(DatabaseMiddleware())
    dp.my_chat_member.outer_middleware(DatabaseMiddleware())

    # User
    dp.message.outer_middleware(UserAccountMiddleware())
    dp.callback_query.outer_middleware(UserAccountMiddleware())
    dp.my_chat_member.outer_middleware(UserAccountMiddleware())

    # Translator
    dp.message.outer_middleware(TranslatorMiddleware())
    dp.callback_query.outer_middleware(TranslatorMiddleware())


@inject
async def on_startup(dispatcher: Dispatcher = Provide[AppContainer.dp]) -> None:
    """
    On bot startup

    :param dispatcher: Dispatcher
    """

    configure_logging()

    set_dispatcher_injections()

    register_middlewares()

    scheduler: AsyncIOScheduler = dispatcher["scheduler"]

    scheduler.start()

    logging.debug("Bot started")


@inject
async def on_shutdown(
        dispatcher: Dispatcher = Provide[AppContainer.dp],
        bot: Bot = Provide[AppContainer.bot]
) -> None:
    """
    On bot shutdown

    :param dispatcher: Dispatcher
    :param bot: Bot instance
    """

    await bot.session.close()
    await dispatcher.storage.close()

    logging.debug("Bot stopped")
