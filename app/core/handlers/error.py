import logging
from aiogram.types.error_event import ErrorEvent
from aiogram import Router


async def handle_error(event: ErrorEvent) -> None:
    logging.error("Error caused by %s", event.exception, exc_info=True)


def register() -> Router:
    router = Router()

    router.error.register(handle_error)

    return router
