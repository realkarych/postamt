import ormsgpack


def to_bytes(data: dict) -> bytes:
    """Converts a dictionary to bytes using ormsgpack."""
    return ormsgpack.packb(data)


def from_bytes(data: bytes) -> dict:
    """Converts bytes to a dictionary using ormsgpack."""
    return ormsgpack.unpackb(data)


# 1. Модуль, который фетчит базу и отправляет в кафку_1 данные для авторизации
# 2. Модуль, который берет из кафки_1 данные для авторизации и фетчит письма; кладет объекты писем в топик для отправки.
# 3. Модуль, который фетчит кафку и отправляет письма в кафку_2
# 4. Скедулер смотрит, пуста ли кафка_1, если пуста, то выполнить с шага 1.
