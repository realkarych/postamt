from pathlib import Path, PurePath
from typing import Final

ROOT_DIR: Final[Path] = Path(__file__).parent.parent.parent
WORKING_DIR: Final[Path] = Path(__file__).parent.parent
LOCALES_DIR: Final[PurePath] = PurePath(WORKING_DIR / "locales")
TEMPORARY_ATTACHMENTS_DIR: Final[PurePath] = PurePath(ROOT_DIR / ".cache")

LOGO_IMAGE_PATH: Final[PurePath] = PurePath(WORKING_DIR / "assets" / "logo.jpg")
