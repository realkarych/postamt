import flet as f

from app.utils import paths


async def _start_app(page: f.Page) -> None:
    page.title = "Email"
    page.theme_mode = f.ThemeMode.LIGHT
    page.fonts = {"montserrat": str(paths.FONTS_DIR_PATH / "montserrat.ttf")}
    page.theme = f.Theme(
        font_family="montserrat",
    )
    await page.add_async(f.Text("Email topic", size=24))
    await page.add_async(f.Text("Текст", size=16))
    await page.add_async(f.Text("От кого", size=12))
    await page.add_async(f.Text("Дата", size=12))


async def start(host: str, port: int) -> None:
    await f.app_async(target=_start_app, host=host, port=port)
