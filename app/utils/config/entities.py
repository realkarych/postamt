from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BotConfig:
    token: str
    default_locale: str
    logging_level: str
