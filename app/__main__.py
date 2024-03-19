"""App launcher"""

import asyncio
import logging

import tzlocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from app.core.handlers import factory

from app.core.handlers.private_chat import (
    base_commands as base_handlers,
    email_auth as email_auth_handlers,
)
from app.core.handlers.forum import triggers as forum_triggers
from app.core.handlers import error as error_handlers
from app.core.middlewares.db import DbSessionMiddleware
from app.core.middlewares.fernet_keys import FernetKeysMiddleware
from app.core.commands.command import set_bot_commands
from app.services.broker import topics
from app.services.broker.email_broker import EmailBroker
from app.services.cryptography.cryptographer import EmailCryptographer
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

    SimpleI18nMiddleware(i18n).setup(dp)

    dp.message.middleware(FernetKeysMiddleware(configloader.fernet_keys))
    dp.my_chat_member.middleware(FernetKeysMiddleware(configloader.fernet_keys))
    dp.callback_query.middleware(FernetKeysMiddleware(configloader.fernet_keys))
    dp.edited_message.middleware(FernetKeysMiddleware(configloader.fernet_keys))

    dp.message.middleware(DbSessionMiddleware(session_pool))
    dp.my_chat_member.middleware(DbSessionMiddleware(session_pool))
    dp.callback_query.middleware(DbSessionMiddleware(session_pool))
    dp.edited_message.middleware(DbSessionMiddleware(session_pool))

    kafka_producer = AIOKafkaProducer(bootstrap_servers=f"{configloader.kafka.host}:{configloader.kafka.port}")
    kafka_consumer_email = AIOKafkaConsumer(
        topics.EMAIL, bootstrap_servers=f"{configloader.kafka.host}:{configloader.kafka.port}"
    )
    kafka_consumer_msg = AIOKafkaConsumer(
        topics.MSG, bootstrap_servers=f"{configloader.kafka.host}:{configloader.kafka.port}"
    )
    await kafka_producer.start()
    await kafka_consumer_email.start()
    await kafka_consumer_msg.start()

    email_broker = EmailBroker(
        producer=kafka_producer,
        sessionmaker=session_pool,
        email_crypto=EmailCryptographer(fernet_key=configloader.fernet_keys[configloader.consts.FernetIDs.EMAIL]),
    )

    scheduler = _init_scheduler()

    scheduler.add_job(
        email_broker.start,
        IntervalTrigger(seconds=1),
    )

    # ------------ Provide your handler-modules here: ------------
    factory.register(
        dp,
        error_handlers,
        email_auth_handlers,
        forum_triggers,
        # This module should be the last one, because it contains handler of unexpected messages
        base_handlers,
    )
    # ------------------------------------------------------------

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()

        await email_broker.stop()
        scheduler.remove_all_jobs()
        scheduler.shutdown()
        await kafka_producer.stop()
        await kafka_consumer_email.stop()
        await kafka_consumer_msg.stop()


def _init_scheduler() -> AsyncIOScheduler:
    """
    Initialize & start scheduler.
    """
    scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
    scheduler.start()
    return scheduler


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
