from typing import Any, Callable, Coroutine
from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import (
    ChatMemberUpdatedFilter,
    ADMINISTRATOR,
    IS_NOT_MEMBER,
    MEMBER,
    KICKED,
    LEFT,
    RESTRICTED,
    CREATOR,
)
from aiogram.types import ChatMemberUpdated, ChatMemberOwner
from contextlib import suppress
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.i18n import gettext as _


def chat_is_forum(handler: Callable) -> Callable[[ChatMemberUpdated, Bot, Any], Coroutine]:
    async def wrapper(event: ChatMemberUpdated, bot: Bot, *args, **kwargs):
        if event.chat.is_forum:
            return await handler(event, bot, *args, **kwargs)

        with suppress(TelegramBadRequest):
            await bot.send_message(
                chat_id=await _get_owner_id(event, bot),
                text=_(
                    "Chat <b>{chat_title}</b> is not a forum...\nCheck the "
                    '<a href="https://blog.karych.ru/postamt-forum-setup">guideline</a> and try again '
                    "(remove bot from this group and add again).",
                ),
            )
        return

    return wrapper


async def _get_owner_id(event: ChatMemberUpdated, bot: Bot) -> int:
    chat_admins = await bot.get_chat_administrators(chat_id=event.chat.id)
    for admin in chat_admins:
        if isinstance(admin, ChatMemberOwner) and not admin.user.is_bot:
            return admin.user.id
    return chat_admins[0].user.id


@chat_is_forum
async def bot_added_to_forum(event: ChatMemberUpdated, bot: Bot, session: AsyncSession):
    pass


def register() -> Router:
    router = Router()

    router.my_chat_member.register(
        bot_added_to_forum,
        ChatMemberUpdatedFilter(
            member_status_changed=(IS_NOT_MEMBER | MEMBER | KICKED | LEFT | RESTRICTED) >> (ADMINISTRATOR | CREATOR)
        ),
    )

    return router
