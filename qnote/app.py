from textual.app import App

from qnote import themes
from qnote.modes.settings import SettingsScreen
from qnote.modes.main import MainScreen
from qnote.utils import init_db, load_all_settings, get_setting


class QnoteApp(App):
    """A Textual app to easily take and manage notes."""

    AUTO_FOCUS = "#sidebar"
    CSS_PATH = "default.tcss"
    TITLE = "QNote"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
    ]

    MODES = {
        "main": MainScreen,
        "settings": SettingsScreen,
    }

    SCREENS = {
        "main_screen": MainScreen,
        "settings_screen": SettingsScreen,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        init_db()
        load_all_settings()

    def on_mount(self):
        self.switch_mode("main")
        for theme in themes.all_themes:
            self.register_theme(theme)
        self.theme = get_setting("theme", "qnote")


if __name__ == "__main__":
    app = QnoteApp()
    app.run()
