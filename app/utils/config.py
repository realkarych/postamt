import pydantic_settings
from app.utils import paths
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings
from typing import Final, Optional

class BotConfig(BaseModel):
    """Bot config"""

    token: str
    default_locale: str = "en"
    parse_mode: str = "HTML"


class DBConfig(BaseModel):
    """Database config"""

    host: Optional[str] = None
    port: Optional[int] = None
    name: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None

    def get_uri(self) -> str:
        """Returns URI of PostgreSQL database"""
        dsn = PostgresDsn.build(  # type: ignore
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )
        return str(dsn)


class Config(BaseSettings):
    """App config"""

    BOT_TOKEN: str
    BOT_DEFAULT_LOCALE: str = "en"

    APP_LOGGING_LEVEL: str = "DEBUG"

    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str = "postamt"
    DB_USER: str
    DB_PASSWORD: str

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
