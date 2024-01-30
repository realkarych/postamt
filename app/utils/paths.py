from pathlib import Path, PurePath
from typing import Final

ROOT_DIR: Final[Path] = Path(__file__).parent.parent.parent
WORKING_DIR: Final[Path] = Path(__file__).parent.parent
LOCALES_DIR: Final[PurePath] = PurePath(WORKING_DIR / "locales")