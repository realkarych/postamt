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

    POSTGRES_HOST: str = getenv("POSTGRES_HOST", "172.16.11.125")
    POSTGRES_PORT: int = int(getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = getenv("POSTGRES_DB", "postamt")
    POSTGRES_USER: str = getenv("POSTGRES_USER", "docker")
    POSTGRES_PASSWORD: str = getenv("DB_PASSWORD", "")

    class Config:
        env_file = paths.ROOT_DIR / ".env"
        env_file_encoding = "utf-8"

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


config: Final[Config] = Config()
