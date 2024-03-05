# type: ignore[reportOptionalMemberAccess]

from aiogram import types, Router, exceptions
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from pydantic import validate_email

from app.core.filters.chat_type import ChatTypeFilter
from app.core.keyboards import inline, reply
from app.core.states import base_menu, email_register
from app.entities import email as email_entities

from app.services.email.imap.repository import ImapRepository
from app.services.email.imap.session import ImapSession
from app.exceptions.email import ImapConnectionFailed


async def btn_add_email(m: types.Message, state: FSMContext) -> None:
    await state.set_state(state=email_register.EmailRegister.server)
    await m.delete()
    await m.answer(text=_("<b>Let's connect your Email!</b>"), reply_markup=reply.email_reg_pipeline_menu())
    await m.answer(text=_("🏤 Choose your Email server:"), reply_markup=inline.email_servers_keyboard())


async def btn_select_email_server(
    c: types.CallbackQuery, state: FSMContext, callback_data: email_entities.EmailServerCallbackFactory
) -> None:
    await state.set_state(state=email_register.EmailRegister.email)
    email_server = email_entities.get_server_by_id(callback_data.server_id)
    await c.message.edit_text(
        text=_(
            "🏤 <i>Email server:</i> {email_server_title}\n"
            "📬 <i>Email address:</i> ____\n"
            "🗝️ <i>Email access key:</i> ____\n\n"
            "<b>Now, enter your Email address:</b>".format(email_server_title=email_server.value.title)
        ),
    )
    await state.update_data(data={"email_server": email_server, "email_msg_id": c.message.message_id})


async def handle_entered_email(m: types.Message, state: FSMContext) -> None:
    await m.delete()
    email_str = m.text.strip()
    try:
        validate_email(email_str)
    except ValueError:
        await m.answer(
            text=_("❌ Invalid email address: {email_str}!\n\n<b>Try again:</b>").format(email_str=email_str)
        )
        return
    await state.set_state(state=email_register.EmailRegister.password)
    await state.update_data(data={"email_address": email_str})
    msg = await _edit_or_create_msg(
        message=m,
        to_edit_msg_id=(await state.get_data()).get("email_msg_id"),
        text=_(
            "🏤 <i>Email server:</i> {email_server_title}\n"
            "📬 <i>Email address:</i> {email_address}\n"
            "🗝️ <i>Email access key:</i> ____\n\n"
            "<b>Now, enter your Email access key:</b>"
        ).format(email_server_title=(await state.get_data()).get("email_server").value.title, email_address=email_str),
    )
    await state.update_data(data={"email_msg_id": msg.message_id})


async def handle_entered_password(m: types.Message, state: FSMContext) -> None:
    await m.delete()
    password = m.text.strip()
    state_data = await state.get_data()
    if await can_estabilish_connection(
        email_server=state_data.get("email_server"),
        email_address=state_data.get("email_address"),
        email_password=password,
    ):
        await _edit_or_create_msg(
            message=m,
            to_edit_msg_id=state_data.get("email_msg_id"),
            text=_(
                "🏤 <i>Email server:</i> {email_server_title}\n"
                "📬 <i>Email address:</i> {email_address}\n"
                "🗝️ <i>Email access key:</i> {}\n\n"
                "🎉 <b>Congrats, Email connected!</b>"
            ),
        )

    else:
        await m.answer(
            text=_("❌ Invalid email access key: {email_password}!\n\n<b>Try again:</b>").format(
                email_password=password
            )
        )


async def can_estabilish_connection(
    email_server: email_entities.EmailServers, email_address: str, email_password: str
) -> bool:
    try:
        async with ImapSession(
            server=email_server, auth_data=email_entities.EmailAuthData(email=email_address, password=email_password)
        ) as imap_session:
            repo = ImapRepository(session=imap_session, user=email_entities.EmailUser(email=email_address))
            repo.get_first_email_ids(1)
        return True
    except ImapConnectionFailed:
        return False


async def _edit_or_create_msg(message: types.Message, to_edit_msg_id: int, text: str, **kwargs) -> types.Message:
    try:
        await message.bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=to_edit_msg_id,
            text=text,
            **kwargs,
        )
        return message
    except exceptions.TelegramBadRequest:
        return await message.answer(
            text=text,
            **kwargs,
        )


def register() -> Router:
    router = Router()
    router.message.filter(ChatTypeFilter(chat_type=ChatType.PRIVATE))

    router.message.register(
        btn_add_email,
        base_menu.BaseMenu.register_email,
    )

    router.callback_query.register(
        btn_select_email_server,
        email_entities.EmailServerCallbackFactory.filter(),
    )

    router.message.register(
        handle_entered_email,
        email_register.EmailRegister.email,
    )

    router.message.register(handle_entered_password, email_register.EmailRegister.password)

    return router
