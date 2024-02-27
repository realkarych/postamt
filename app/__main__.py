"""App launcher"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware

from app.core.handlers import factory
from app.core.handlers.private_chat import base as base_handlers
from app.core.handlers import error as error_handlers
from app.core.middlewares.db import DbSessionMiddleware
from app.core.commands.command import set_bot_commands
from app.services.database.connector import setup_get_pool
from app.utils import paths
from app.utils.config import config


async def main() -> None:
    """Run app"""

    logging.basicConfig(
        level=config.APP_LOGGING_LEVEL,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(config.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    i18n = I18n(
        path=str(paths.LOCALES_DIR),
        default_locale=config.BOT_DEFAULT_LOCALE,
        domain="bot",
    )
    session_pool = await setup_get_pool(db_uri=config.build_postgres_dsn())

    dp.message.middleware(SimpleI18nMiddleware(i18n))
    dp.callback_query.middleware(SimpleI18nMiddleware(i18n))

    dp.message.middleware(DbSessionMiddleware(session_pool))
    dp.callback_query.middleware(DbSessionMiddleware(session_pool))
    dp.edited_message.middleware(DbSessionMiddleware(session_pool))

    # Provide your handlers here:
    factory.register(
        dp,
        error_handlers,
        base_handlers,
    )

    await set_bot_commands(bot=bot)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
