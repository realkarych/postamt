import logging
from aiogram import types, Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.filters.chat_type import ChatTypeFilter
from app.core.commands.command import PrivateChatCommands
from app.entities.email import EmailAuthData, EmailServers, EmailUser
from app.entities.user import User
from app.services.database.dao.user import UserRepository

from app.services.email.imap.repository import ImapRepository as ImapRepo

from app.services.email.imap.session import ImapSession


_DEBUG_EMAIL = "postamt.bot@yandex.ru"
_DEBUG_NAME = "POSTAMT"
_DEBUG_PASSWORD = "wethufafnpmcpihp"


async def cmd_start(m: types.Message, session: AsyncSession, state: FSMContext) -> None:
    await state.clear()

    user = User.from_message(message=m)
    repo = UserRepository(session=session)

    await repo.add_user(user)
    await repo.commit()

    await m.answer(text=_("<b>Hello, {first_name}!</b>").format(first_name=user.first_name))
    async with ImapSession(
        server=EmailServers.YANDEX,
        auth_data=EmailAuthData(
            email=_DEBUG_EMAIL,
            password=SecretStr(_DEBUG_PASSWORD),
        ),
    ) as imap_session:
        repo = ImapRepo(session=imap_session, user=EmailUser(email=_DEBUG_EMAIL, name=_DEBUG_NAME))
        async for email in repo.fetch_emails(email_ids=await repo.get_last_email_ids(3)):
            logging.info(email)


def register() -> Router:
    router = Router()

    router.message.register(
        cmd_start,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        Command(str(PrivateChatCommands.start)),
    )

    return router
