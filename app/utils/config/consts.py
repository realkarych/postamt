from typing import Final
from enum import Enum


FERNET_KEYS_ENCODING: Final[str] = "utf-8"


class FernetIDs(Enum):
    EMAIL = "email"
    TOPIC = "topic"

    def __str__(self) -> str:
        return self.value


EMAIL_CHUNK_LIMIT: Final[int] = 15
EMAIL_CONNECTION_ATTEMPTS: Final[int] = 10
EMAIL_CONNECTION_ATTEMPTS_DELAY: Final[float] = 0.1  # in seconds
