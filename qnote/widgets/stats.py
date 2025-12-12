from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalGroup, Vertical
from textual.reactive import reactive
from textual.widgets import Label, Static

from qnote.widgets.lumens import Lumen


class Stats(Static, can_focus=False):
    """Stats and Visuals."""

    wordcount = Static()
    created = Static()
    updated = Static()
    age = Static()
    lumen = Lumen(id="lumen")

    note_id = reactive(None)

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical():
                with HorizontalGroup():
                    yield Label("Created on: ")
                    yield self.created
                with HorizontalGroup():
                    yield Label("Updated on: ")
                    yield self.updated
                with HorizontalGroup():
                    yield Label("Wordcount: ")
                    yield self.wordcount
                with HorizontalGroup():
                    yield Label("Age: ")
                    yield self.age
            with Vertical():
                with HorizontalGroup():
                    yield self.lumen

    def load_data(self, data: object) -> None:
        """Load note content to the widget."""
        try:
            self.note_id = data["id"]
            self.wordcount.content = str(len(data["content"].split()))
            self.created.content = str(data["created"])
            self.updated.content = str(data["updated"])
            self.age.content = str(datetime.now() - data["created"])
        except TypeError:
            pass
            # TODO: logging

    def on_mount(self) -> None:
        self.border_title = "Stats"
        self.disabled = True
