from aiogram.types import InlineKeyboardMarkup

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.entities.email import EmailServerCallbackFactory, EmailServers


def email_servers_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=EmailServers.GMAIL.value.title,
        callback_data=EmailServerCallbackFactory(server_id=EmailServers.GMAIL.value.id_),
    )
    builder.button(
        text=EmailServers.OUTLOOK.value.title,
        callback_data=EmailServerCallbackFactory(server_id=EmailServers.OUTLOOK.value.id_),
    )
    builder.button(
        text=EmailServers.OFFICE365.value.title,
        callback_data=EmailServerCallbackFactory(server_id=EmailServers.OFFICE365.value.id_),
    )

    builder.button(
        text=EmailServers.YANDEX.value.title,
        callback_data=EmailServerCallbackFactory(server_id=EmailServers.YANDEX.value.id_),
    )
    builder.button(
        text=EmailServers.MAILRU.value.title,
        callback_data=EmailServerCallbackFactory(server_id=EmailServers.MAILRU.value.id_),
    )

    builder.button(
        text=EmailServers.ICLOUD.value.title,
        callback_data=EmailServerCallbackFactory(server_id=EmailServers.ICLOUD.value.id_),
    )
    builder.button(
        text=EmailServers.YAHOO.value.title,
        callback_data=EmailServerCallbackFactory(server_id=EmailServers.YAHOO.value.id_),
    )

    builder.adjust(3, 2, 2)

    return builder.as_markup()
