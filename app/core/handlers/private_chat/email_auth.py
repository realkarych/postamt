# type: ignore[reportOptionalMemberAccess]

from aiogram import types, Router
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from app.core.filters.chat_type import ChatTypeFilter
from app.core.keyboards import inline, reply
from app.core.states import base_menu, email_register
from app.entities.email import EmailServerCallbackFactory


async def btn_add_email(m: types.Message, state: FSMContext) -> None:
    await state.set_state(state=email_register.EmailRegister.server)
    await m.bot.delete_message(chat_id=m.from_user.id, message_id=m.message_id)
    msg = await m.answer(text=_("📬 Choose your Email server:"), reply_markup=inline.email_servers_keyboard())
    await state.set_data(data={"pipeline_msg_ids": [msg.message_id]})


async def btn_select_email_server(
    c: types.CallbackQuery, state: FSMContext, server_callback: EmailServerCallbackFactory
) -> None:
    await state.set_state(state=email_register.EmailRegister.email)
    await state.update_data(data={"server": server_callback.server})
    await c.message.edit_reply_markup(None)
    await c.message.answer(text=_("📧 Enter your Email address:"), reply_markup=reply.email_reg_pipeline_menu())


def register() -> Router:
    router = Router()

    router.message.register(
        btn_add_email,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        base_menu.BaseMenu.register_email,
    )

    router.callback_query.register(
        btn_select_email_server, ChatTypeFilter(chat_type=ChatType.PRIVATE), EmailServerCallbackFactory.filter()
    )

    return router
