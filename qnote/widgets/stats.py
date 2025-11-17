from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive
from textual.widgets import Input, Label, Static

from utils import get_notes, update_note_category, update_note_title


class Stats(Static, can_focus=False):
    """Stats and or To-Do."""

    wordcount = Static()

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label("Wordcount:")
            yield self.wordcount

    note_id = reactive(None)

    def load_data(self, data: object) -> None:
        """Load note content to the widget."""
        try:
            self.note_id = data[0]
            self.wordcount.content = str(len(data[2].split()))
        except TypeError:
            pass
            # self.border_title = str(data)  # TODO: something better in here
            # self.disabled = True

    def on_mount(self) -> None:
        self.border_title = "Stats"
        self.disabled = True
