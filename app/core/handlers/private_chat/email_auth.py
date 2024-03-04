# type: ignore[reportOptionalMemberAccess]

from aiogram import types, Router
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from app.core.filters.chat_type import ChatTypeFilter
from app.core.keyboards import inline, reply
from app.core.states import base_menu, email_register
from app.entities import email as email_entities


async def btn_add_email(m: types.Message, state: FSMContext) -> None:
    await state.set_state(state=email_register.EmailRegister.server)
    await m.bot.delete_message(chat_id=m.from_user.id, message_id=m.message_id)
    await m.answer(text=_("🏤 Choose your Email server:"), reply_markup=inline.email_servers_keyboard())


async def btn_select_email_server(
    c: types.CallbackQuery, state: FSMContext, callback_data: email_entities.EmailServerCallbackFactory
) -> None:
    await state.set_state(state=email_register.EmailRegister.email)
    email_server = email_entities.get_server_by_id(callback_data.server_id)
    await state.update_data(data={"server_id": email_server})
    await c.bot.delete_message(c.from_user.id, c.message.message_id)
    await c.message.answer(
        text=_(
            "🏤 <i>Email server:</i> {email_server_title}\n"
            "📬 <i>Email address:</i> ---\n"
            "🗝️ <i>Email access key:</i> ---\n\n"
            "<b>Now, enter your Email address:</b>"
            .format(email_server_title=email_server.title)
        ), reply_markup=reply.email_reg_pipeline_menu()
    )


def register() -> Router:
    router = Router()

    router.message.register(
        btn_add_email,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        base_menu.BaseMenu.register_email,
    )

    router.callback_query.register(
        btn_select_email_server,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        email_entities.EmailServerCallbackFactory.filter(),
    )

    return router
