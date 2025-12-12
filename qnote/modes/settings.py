from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalGroup, VerticalGroup
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Footer, Label, Select, Header, Rule

from qnote.utils import get_setting, set_setting

class LumenSelect(Widget):

    class LumenChanged(Message, bubble=True):
        """Sent when the 'lumen' changes."""

        def __init__(self, value: str) -> None:
            super().__init__()
            self.value = value

    options = [
        ("None", "none"),
        ("QNote", "qnote"),
        #("Waves", "waves"),
        #("Pulse", "pulse"),
        ("Snake", "snake")
    ]

    select_lumen: Select[str] = Select(options, classes="setting-select", id="select-lumen", allow_blank=False, compact=True)

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label("Lumen:", classes="setting-label")
            yield self.select_lumen

    def on_mount(self) -> None:
        self.select_lumen.value = get_setting("lumen", "qnote")

    def on_select_changed(self, event: Select.Changed) -> None:
        self.post_message(self.LumenChanged(event.value))
        set_setting("lumen", event.value)


class ThemeSelect(Widget):

    class ThemeChanged(Message, bubble=True):
        """Sent when the 'theme' changes."""

        def __init__(self, value: str) -> None:
            super().__init__()
            self.value = value

    options = [
        ("QNote", "qnote"),
        ("Gruvbox", "gruvbox"),
        ("Nord", "nord"),
        ("solarized-light", "solarized-light"),
    ]

    select_theme = reactive(None)

    def compose(self) -> ComposeResult:
        #self.options = [(name, name) for name in self.app.available_themes]
        self.select_theme = Select(self.options, classes="setting-select", id="select-theme", allow_blank=False,
                                           compact=True)
        with HorizontalGroup():
            yield Label("Theme:", classes="setting-label")
            yield self.select_theme

    def on_mount(self) -> None:
        self.select_theme.value = get_setting("theme", "qnote")

    def on_select_changed(self, event: Select.Changed) -> None:
        set_setting("theme", event.value)
        self.app.theme = event.value


class SettingsScreen(Screen):

    def __init__(self) -> None:
        super().__init__()
        self.title = "Settings"

    BINDINGS = [
        ("escape", "app.switch_mode('main')", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Horizontal():
            with VerticalGroup(classes="setting-column"):
                yield LumenSelect(classes="setting-element")
                yield Rule(classes="setting-element")
                yield ThemeSelect(classes="setting-element")
            #with VerticalGroup(classes="setting-column"):
            #    yield Label("Future Release")
            #with VerticalGroup(classes="setting-column"):
            #    yield Label("Future Release")
