from aiogram import types, Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession
from app import consts

from app.core.filters.chat_type import ChatTypeFilter
from app.core.commands.command import PrivateChatCommands
from app.core.keyboards import reply
from app.entities.user import User
from app.services.database.repositories.user import UserRepo

import logging


async def cmd_start(m: types.Message, session: AsyncSession, state: FSMContext) -> None:
    await state.clear()

    user = User.from_message(message=m)

    repo = UserRepo(session=session)

    try:
        await repo.add_user(user=user, update_when_exists=True)
    except Exception as e:
        logging.error(e)
        await m.answer(
            text=_(
                '😔 Sorry, but an error occurred while processing your request. '
                'Please try again later.\nIf the problem persists, write to the {group_username}.'
            ).format(group_username=consts.GROUP_USERNAME)
        )
        return

    await m.answer(
        text=_(
            '👋 <b>Hello, {firstname}!</b>\n\n'
            'POSTAMT is an Email client powered by Forums and WebApps.\n\n'
            'To use bot, follow {channel_username}. We\'ll use it to let you '
            'know about important changes in the project.\n<i>The bot, in turn, '
            'will never send advertising or service notifications.</i>'
        ).format(firstname=user.firstname, channel_username=consts.CHANNEL_USERNAME),
        reply_markup=reply.base_menu(),
    )


async def cmd_help(m: types.Message) -> None:
    await m.answer(
        text=_(
            '- If you have trouble setting up the Bot or you found a bug, '
            'write to {group_username}. Priority language is english.\n'
            '- If you want to contribute to Bot, check the <a href="{repo_link}">repository</a>.'
        ).format(group_username=consts.GROUP_USERNAME, repo_link=consts.REPO_LINK)
    )


async def unexpected_input(m: types.Message) -> None:
    await m.reply(text=_('🤔 Unexpected input...'))


def register() -> Router:
    router = Router()
    router.message.filter(ChatTypeFilter(chat_type=ChatType.PRIVATE))

    router.message.register(
        cmd_start,
        Command(str(PrivateChatCommands.start)),
    )

    router.message.register(
        cmd_help,
        Command(str(PrivateChatCommands.help)),
    )

    router.message.register(
        unexpected_input,
    )

    return router
