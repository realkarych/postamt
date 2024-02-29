from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.utils.config import consts


class FernetKeysMiddleware(BaseMiddleware):

    def __init__(self, fernet_keys: dict[consts.FernetIDs, bytes]):
        super().__init__()
        self._fernet_keys = fernet_keys

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["fernet_keys"] = self._fernet_keys
        return await handler(event, data)
