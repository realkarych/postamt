import configparser
import os

from app.settings import paths
from pydantic import BaseModel, PostgresDsn, field_validator
from typing import Optional


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

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def get_uri(self) -> str:
        """Returns URI of PostgreSQL database"""
        return PostgresDsn.build(  # type: ignore
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=f"/{self.name}",
        )


class Config(BaseModel):
    """Configurator"""
    bot: BotConfig
    db: DBConfig


def load_config() -> Config:
    """Load and return bot configuration data"""

    config_file_path = paths.ROOT_DIR / "app.ini"

    if not os.path.exists(config_file_path):
        raise ValueError("app.ini wasn't created!")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    bot = config["bot"]
    db = config["db"]

    return Config(
        bot=BotConfig(
            token=bot["token"],
            default_locale=bot["default_locale"],
        ),
        db=DBConfig(
            host=db["host"],
            port=int(db["port"]),
            name=db["name"],
            user=db["user"],
            password=db["password"]
        )
    )
