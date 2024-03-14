from functools import wraps
from typing import Any, Callable, Coroutine
from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
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
from aiogram.types import FSInputFile
from app.utils import paths
from app.utils.config.consts import FernetIDs

from app.services.cryptography.cryptographer import EmailCryptographer
from app.services.database.repositories.email import EmailRepo


def chat_is_forum(handler: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
    @wraps(handler)
    async def wrapper(
        event: ChatMemberUpdated, bot: Bot, session: AsyncSession, fernet_keys: dict[FernetIDs, bytes]
    ) -> Any:
        if event.chat.is_forum:
            return await handler(event, bot, session, fernet_keys)

        with suppress(TelegramBadRequest):
            await bot.send_message(
                chat_id=await get_owner_id(event, bot),
                text=_(
                    "Chat <b>{chat_title}</b> is not a forum...\nCheck the "
                    '<a href="https://blog.karych.ru/postamt-forum-setup">guideline</a> and try again '
                    "(remove bot from this group and add again).",
                ).format(chat_title=event.chat.title),
            )
        return

    return wrapper


async def get_owner_id(event: ChatMemberUpdated, bot: Bot) -> int:
    chat_admins = await bot.get_chat_administrators(chat_id=event.chat.id)
    for admin in chat_admins:
        if isinstance(admin, ChatMemberOwner) and not admin.user.is_bot:
            return admin.user.id
    return chat_admins[0].user.id


@chat_is_forum
async def bot_added_to_forum(
    event: ChatMemberUpdated, bot: Bot, session: AsyncSession, fernet_keys: dict[FernetIDs, bytes]
):
    owner_id = await get_owner_id(event, bot)
    email_repo = EmailRepo(session=session, crypto=EmailCryptographer(fernet_key=fernet_keys[FernetIDs.EMAIL]))

    emailbox = await email_repo.get_emailbox_without_forum(owner_id)
    if not emailbox:
        await bot.send_message(
            chat_id=owner_id,
            text=_(
                "🚫 <b>Bot was added to the forum <b>{chat_title}</b>, but you have no connected emailbox.\n\n"
                "Please, add an emailbox to the bot in private messages and try again.",
            ).format(chat_title=event.chat.title),
        )
        return
    emailbox = emailbox.decrypt()

    if not emailbox.db_id:
        raise ValueError("Emailbox db_id is not set in db or not decrypted")

    await email_repo.update_forum_id(emailbox_id=emailbox.db_id, forum_id=event.chat.id)
    await bot.send_message(
        chat_id=owner_id,
        text=_(
            "🎉 <b>Bot was added to the forum {chat_title}</b>.\n\n"
            "Bot will setup the forum and fetch some emails.\n\n"
            "Bot will notify you when it's done.\n<i>It may take a while...</i>",
        ).format(chat_title=event.chat.title),
    )
    await _update_forum_settings(event, bot)


async def _update_forum_settings(event: ChatMemberUpdated, bot: Bot) -> None:
    with suppress(TelegramBadRequest, TelegramForbiddenError):
        await bot.set_chat_photo(chat_id=event.chat.id, photo=FSInputFile(path=str(paths.LOGO_IMAGE_PATH)))

    with suppress(TelegramBadRequest, TelegramForbiddenError):
        await bot.edit_general_forum_topic(chat_id=event.chat.id, name=_("Send Email"))


def register() -> Router:
    router = Router()

    router.my_chat_member.register(
        bot_added_to_forum,
        ChatMemberUpdatedFilter(
            member_status_changed=(IS_NOT_MEMBER | MEMBER | KICKED | LEFT | RESTRICTED) >> (ADMINISTRATOR | CREATOR)
        ),
    )

    return router
