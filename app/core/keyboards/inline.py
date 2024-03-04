from aiogram.types import InlineKeyboardMarkup

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.entities.email import EmailServerCallbackFactory, EmailServers


def email_servers_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=EmailServers.GMAIL.value.title, callback_data=EmailServerCallbackFactory(server=EmailServers.GMAIL.value)
    )
    builder.button(
        text=EmailServers.OUTLOOK.value.title,
        callback_data=EmailServerCallbackFactory(server=EmailServers.OUTLOOK.value),
    )
    builder.button(
        text=EmailServers.OFFICE365.value.title,
        callback_data=EmailServerCallbackFactory(server=EmailServers.OFFICE365.value),
    )

    builder.adjust()

    builder.button(
        text=EmailServers.YANDEX.value.title,
        callback_data=EmailServerCallbackFactory(server=EmailServers.YANDEX.value),
    )
    builder.button(
        text=EmailServers.MAILRU.value.title,
        callback_data=EmailServerCallbackFactory(server=EmailServers.MAILRU.value),
    )

    builder.adjust()

    builder.button(
        text=EmailServers.ICLOUD.value.title,
        callback_data=EmailServerCallbackFactory(server=EmailServers.ICLOUD.value),
    )
    builder.button(
        text=EmailServers.YAHOO.value.title, callback_data=EmailServerCallbackFactory(server=EmailServers.YAHOO.value)
    )

    return builder.as_markup()
