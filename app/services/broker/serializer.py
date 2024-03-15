import ormsgpack


def to_bytes(data: dict) -> bytes:
    """Converts a dictionary to bytes using ormsgpack."""
    return ormsgpack.packb(data)


def from_bytes(data: bytes) -> dict:
    """Converts bytes to a dictionary using ormsgpack."""
    return ormsgpack.unpackb(data)
