from typing import Final
from enum import Enum


FERNET_KEYS_ENCODING: Final[str] = "utf-8"


class FernetIDs(Enum):
    EMAIL = "email"
    TOPIC = "topic"

    def __str__(self) -> str:
        return self.value
