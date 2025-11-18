from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive
from textual.widgets import Label, Static

from utils import get_notes


class Stats(Static, can_focus=False):
    """Stats and or To-Do."""

    wordcount = Static()
    created = Static()
    updated = Static()

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label("Wordcount: ")
            yield self.wordcount
        with HorizontalGroup():
            yield Label("Created on: ")
            yield self.created
        with HorizontalGroup():
            yield Label("Updated on: ")
            yield self.updated

    note_id = reactive(None)

    def load_data(self, data: object) -> None:
        """Load note content to the widget."""
        try:
            self.note_id = data[0]
            self.wordcount.content = str(len(data[2].split()))
            self.created.content = data[5]
            self.updated.content = str(data[6])
        except TypeError:
            pass
            #self.border_title = str(data)  # TODO: something better in here
            # self.disabled = True

    def on_mount(self) -> None:
        self.border_title = "Stats"
        self.disabled = True
