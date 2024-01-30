"""App launcher"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware

from app.core.handlers import factory
from app.core.handlers.private_chat import base
from app.core.middlewares.db import DbSessionMiddleware
from app.core.middlewares.i18n import TranslatorRunnerMiddleware
from app.core.navigations.command import set_bot_commands
from app.services.database.connector import setup_get_pool
from app.settings import paths
from app.settings.config import load_config


async def main() -> None:
    """Starts app & polling."""

    config = load_config()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    bot = Bot(config.bot.token, parse_mode=config.bot.parse_mode)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    i18n = I18n(path=str(paths.LOCALES_DIR), default_locale=config.bot.default_locale, domain="bot")
    session_pool = await setup_get_pool(db_uri=config.db.get_uri())  # type: ignore

    dp.message.middleware(SimpleI18nMiddleware(i18n))
    dp.callback_query.middleware(SimpleI18nMiddleware(i18n))

    dp.message.middleware(DbSessionMiddleware(session_pool))
    dp.callback_query.middleware(DbSessionMiddleware(session_pool))
    dp.edited_message.middleware(DbSessionMiddleware(session_pool))

    dp.message.middleware(TranslatorRunnerMiddleware())
    dp.callback_query.middleware(TranslatorRunnerMiddleware())
    dp.edited_message.middleware(TranslatorRunnerMiddleware())

    # Provide your handlers here:
    factory.register(dp, base, )

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
        # Logging this is pointless
        pass
