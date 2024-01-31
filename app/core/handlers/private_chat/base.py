from aiogram import types, Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.filters.chat_type import ChatTypeFilter
from app.core.navigations.command import PrivateChatCommands
from app.entities.user import User
from app.services.database.dao.user import UserRepository


async def cmd_start(m: types.Message, session: AsyncSession, state: FSMContext) -> None:
    await state.clear()

    user = User.from_message(message=m)
    repo = UserRepository(session=session)

    await repo.add_user(user)
    await repo.commit()

    await m.answer(text=_("Hello, {first_name}!").format(first_name=user.first_name))


def register() -> Router:
    router = Router()

    router.message.register(
        cmd_start,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        Command(str(PrivateChatCommands.start)),
    )

    return router
