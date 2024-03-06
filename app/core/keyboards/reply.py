from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


class ResizedReplyKeyboard(ReplyKeyboardMarkup):
    """
    I (@Karych) prefer override default ReplyKeyboardMarkup to avoid passing
    the resizer parameter every time.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resize_keyboard = True


def base_menu() -> ResizedReplyKeyboard:
    return ResizedReplyKeyboard(
        keyboard=[
            [
                KeyboardButton(text=_("💌 Add Emailbox")),
            ]
        ]
    )


def email_reg_pipeline_menu() -> ResizedReplyKeyboard:
    return ResizedReplyKeyboard(
        keyboard=[
            [
                KeyboardButton(text=_("⮐ Previous step")),
                KeyboardButton(text=_("❌ Cancel action")),
            ]
        ]
    )
