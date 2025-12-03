from textual.app import App
from textual.reactive import Reactive

from . import themes
from .modes.settings import SettingsScreen, LumenSelect
from .modes.main import MainScreen
from .utils import init_db, load_all_settings


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

    lumen_theme = Reactive(None)

    def on_mount(self):
        self.switch_mode("settings")
        for theme in themes.all_themes:
            self.register_theme(theme)
        self.theme = "qnote"

    def on_lumen_select_lumen_changed(self, message: LumenSelect.LumenChanged):  #TODO: changing settings
        # Store the value or apply it immediately
        self.lumen_theme = message.value


if __name__ == "__main__":
    init_db()
    load_all_settings()
    app = QnoteApp()
    app.run()
