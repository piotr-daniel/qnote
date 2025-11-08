from textual.widgets import Static, TextArea
from utils import add_note, load_notes


class Details(TextArea):
    """Note details widget."""

    BINDINGS = [
        ("ctrl+s", "save_note()", "Save Note"),
        ("ctrl+l", "load_note()", "Load Notes"),  #TODO needs to work with the tree
    ]

    def action_save_note(self) -> None:  #TODO needs to save edited note and new func for adding
        """Save note content to DB."""
        add_note("Test", self.text)
        # log success

    def action_load_note(self) -> None:
        """Load note content to the widget."""
        self.text = load_notes()[1]["content"]  #TODO needs to be triggered by tree
        # log success

    def on_mount(self) -> None:
        self.border_title = "Details"

    def on_text_area_changed(self) -> None:
        # self.border_title = self.text
        pass  # for testing purposes, might use in future

class Sidebar(Static, can_focus=True):
    """Sidebar widget."""
    def on_mount(self):
        self.border_title = "Sidebar"


class Stats(Static):
    """Stats and or To-Do."""
    def on_mount(self) -> None:
        self.border_title = "Stats"
