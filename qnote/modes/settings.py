from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalGroup, VerticalGroup
from textual.message import Message
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Footer, Label, Select, Header

from ..utils import get_setting, set_setting, SETTINGS

class LumenSelect(Widget):

    class LumenChanged(Message, bubble=True):
        """Sent when the 'lumen' changes."""

        def __init__(self, value: str) -> None:
            super().__init__()
            self.value = value

    options = [
        ("None", "none"),
        ("QNote", "letter_rain"),
        ("Waves", "waves"),
        ("Pulse", "pulse"),
        ("Snake", "snake")
    ]

    select_lumen: Select[str] = Select(options, id="select-lumen", allow_blank=False, compact=True)

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label("Select Lumen: ", classes="setting-label")
            yield self.select_lumen

    def on_mount(self) -> None:
        self.select_lumen.value = get_setting("lumen")

    def on_select_changed(self, event: Select.Changed) -> None:
        self.post_message(self.LumenChanged(event.value))
        set_setting("lumen", event.value)


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
            with VerticalGroup(classes="setting-column"):
                yield Label("Future Release")
            with VerticalGroup(classes="setting-column"):
                yield Label("Future Release")

    def on_lumen_select_lumen_changed(self, message: LumenSelect.LumenChanged):
        message.stop()
        self.app.post_message(message)
