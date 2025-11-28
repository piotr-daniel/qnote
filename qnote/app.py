from textual.app import App

from . import themes
from .modes.settings import SettingsScreen
from .modes.main import MainScreen
from .utils import init_db


class QnoteApp(App):
    """A Textual app to easily take and manage notes."""

    AUTO_FOCUS = "#sidebar"
    CSS_PATH = "default.tcss"
    TITLE = "QNote"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+s", "switch_mode('settings')", "Settings"),
        ("m", "switch_mode('main')", "Main"),
    ]
    MODES = {
        "main": MainScreen,
        "settings": SettingsScreen,
    }

    def on_mount(self):
        self.switch_mode("main")
        for theme in themes.all_themes:
            self.register_theme(theme)
        self.theme = "qnote"


if __name__ == "__main__":
    init_db()
    app = QnoteApp()
    app.run()
