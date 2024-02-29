"""App launcher"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware

from app.core.handlers import factory
from app.core.handlers.private_chat import base as base_handlers
from app.core.handlers import error as error_handlers
from app.core.middlewares.db import DbSessionMiddleware
from app.core.middlewares.fernet_keys import FernetKeysMiddleware
from app.core.commands.command import set_bot_commands
from app.services.database.connector import setup_get_pool
from app.utils import paths
from app.utils.config import loader as configloader


async def main() -> None:
    """Run app"""

    logging.basicConfig(
        level=configloader.bot_config.logging_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(
        token=configloader.bot_config.token,
        default=DefaultBotProperties(parse_mode="HTML"),
        )
    await set_bot_commands(bot=bot)

    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    i18n = I18n(
        path=str(paths.LOCALES_DIR),
        default_locale=configloader.bot_config.default_locale,
        domain="bot",
    )
    session_pool = await setup_get_pool(db_uri=configloader.postgres_dsn)

    dp.message.middleware(SimpleI18nMiddleware(i18n))
    dp.callback_query.middleware(SimpleI18nMiddleware(i18n))

    dp.message.middleware(FernetKeysMiddleware(configloader.fernet_keys))
    dp.callback_query.middleware(FernetKeysMiddleware(configloader.fernet_keys))

    dp.message.middleware(DbSessionMiddleware(session_pool))
    dp.callback_query.middleware(DbSessionMiddleware(session_pool))
    dp.edited_message.middleware(DbSessionMiddleware(session_pool))

    # ------------ Provide your handlers here: ------------
    factory.register(
        dp,
        error_handlers,
        base_handlers,
    )
    # -----------------------------------------------------

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
