"""
Loads config.
WARNING: Do not import this module anywhere (exclude entry-point — __main__.py).
Provide needed config setting via separated middleware.
"""

from app.utils import paths
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from typing import Final
from os import getenv
from app.utils.config import entities, consts
from app.utils import singleton


@singleton.good_singleton
class AppConfig(BaseSettings):
    """
    Builds app config
    Access in entry-point via config variable
    """

    BOT_TOKEN: str = getenv("BOT_TOKEN", "")
    BOT_DEFAULT_LOCALE: str = getenv("BOT_DEFAULT_LOCALE", "en")
    APP_LOGGING_LEVEL: str = getenv("APP_LOGGING_LEVEL", "DEBUG")

    POSTGRES_HOST: str = getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = getenv("POSTGRES_DB", "postamt")
    POSTGRES_USER: str = getenv("POSTGRES_USER", "docker")
    POSTGRES_PASSWORD: str = getenv("DB_PASSWORD", "")

    EMAIL_FERNET_KEY: bytes = bytes(getenv("EMAIL_FERNET_KEY", ""), encoding=consts.FERNET_KEYS_ENCODING)
    TOPIC_FERNET_KEY: bytes = bytes(getenv("TOPIC_FERNET_KEY", ""), encoding=consts.FERNET_KEYS_ENCODING)

    class Config:
        env_file = paths.ROOT_DIR / ".env"
        env_file_encoding = "utf-8"
        frozen = True

    def build_postgres_dsn(self) -> str:
        """Returns URI of PostgreSQL database"""
        dsn = PostgresDsn.build(  # type: ignore
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
        return str(dsn)


_config = AppConfig()

bot_config: Final[entities.BotConfig] = entities.BotConfig(
    token=_config.BOT_TOKEN, default_locale=_config.BOT_DEFAULT_LOCALE, logging_level=_config.APP_LOGGING_LEVEL
)

postgres_dsn: Final[str] = _config.build_postgres_dsn()

fernet_keys: Final[dict[consts.FernetIDs, bytes]] = {
    consts.FernetIDs.EMAIL: _config.EMAIL_FERNET_KEY,
    consts.FernetIDs.TOPIC: _config.TOPIC_FERNET_KEY,
}
