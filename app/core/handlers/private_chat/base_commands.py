from aiogram import types, Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.filters.chat_type import ChatTypeFilter
from app.core.commands.command import PrivateChatCommands
from app.entities.user import User


async def cmd_start(m: types.Message, session: AsyncSession, state: FSMContext) -> None:
    await state.clear()

    user = User.from_message(message=m)

    await m.answer(
        text=_(
            "👋 <b>Hello, {firstname}!</b>\n\n"
            "POSTAMT is an Email client powered by Forums and WebApps.\n\n"
            "To use bot, follow @postamt_channel. I'll use it to let you "
            "know about important changes in the project. <i>The bot, in turn, "
            "will never send advertising or service notifications.</i>"
        ).format(firstname=user.firstname)
    )


async def cmd_help(m: types.Message, session: AsyncSession, state: FSMContext) -> None:
    await m.answer(
        text=_(
            "- If you have trouble setting up the Bot or you found a bug, "
            "write to @postamt_chat. Priority language is english.\n"
            "- If you want to contribute to Bot, check the "
            "<a href=\"https://github.com/realkarych/postamt\">repository</a>."
        )
    )


def register() -> Router:
    router = Router()

    router.message.register(
        cmd_start,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        Command(str(PrivateChatCommands.start)),
    )

    router.message.register(
        cmd_help, ChatTypeFilter(chat_type=ChatType.PRIVATE), Command(str(PrivateChatCommands.help))
    )

    return router
