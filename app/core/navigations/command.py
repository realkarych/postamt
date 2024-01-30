from enum import Enum, unique

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from pydantic import BaseModel


class Command(BaseModel):
    """Represents wrapper on default Aiogram command"""

    name: str
    description: str

    def to_bot_command(self) -> BotCommand:
        """Map Command object to BotCommand object"""

        return BotCommand(command=self.name, description=self.description)


@unique
class BaseCommandList(Enum):
    """Base list of commands."""

    def __str__(self) -> str:
        return self.value.name

    def __call__(self, *args, **kwargs) -> Command:
        return self.value


class PrivateChatCommands(BaseCommandList):
    """
    List of commands submitted to Telegram menu list.
    Do not implement here admin commands because of submission.
    For this case, create another commands list & factory.
    """

    start = Command(name="start", description="Start Bot")


async def set_bot_commands(bot: Bot) -> None:
    """Creates a commands list in Telegram app menu."""

    # Private chat commands
    await bot.set_my_commands(
        commands=[command().to_bot_command() for command in PrivateChatCommands],
        scope=BotCommandScopeAllPrivateChats()  # pyright: ignore
    )
