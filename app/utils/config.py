from app.utils import paths
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from typing import Final
from os import getenv


class Config(BaseSettings):
    """App config"""

    BOT_TOKEN: str = getenv("BOT_TOKEN", "")
    BOT_DEFAULT_LOCALE: str = getenv("BOT_DEFAULT_LOCALE", "en")
    APP_LOGGING_LEVEL: str = getenv("APP_LOGGING_LEVEL", "DEBUG")

    DB_HOST: str = getenv("DB_HOST", "172.16.11.125")
    DB_PORT: int = int(getenv("DB_PORT", 5432))
    DB_NAME: str = getenv("DB_NAME", "postamt")
    DB_USER: str = getenv("DB_USER", "docker")
    DB_PASSWORD: str = getenv("DB_PASSWORD", "")

    class Config:
        env_file = paths.ROOT_DIR / ".env"
        env_file_encoding = "utf-8"

    def build_postgres_dsn(self) -> str:
        """Returns URI of PostgreSQL database"""
        dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )
        return str(dsn)


config: Final[Config] = Config()  # type: ignore
