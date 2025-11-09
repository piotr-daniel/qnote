from textual.widgets import Static, TextArea, Tree
from textual.widgets.tree import TreeNode
from textual.message import Message
from textual.reactive import reactive
from utils import add_note, load_notes, logging, save_note


class Details(TextArea):
    """Note details widget."""

    BINDINGS = [
        ("ctrl+s", "save_note()", "Save Note"),
    ]

    note_id = reactive(None)
    note_title = reactive(None)

    def load_data(self, data: object) -> None:
        self.note_id = data["id"]
        self.note_title = data["title"]
        self.text = data["content"]

    def action_save_note(self) -> None:  #TODO needs to save edited note and new func for adding
        """Save note content to DB."""
        # add_note("Test", self.text)
        save_note(self.note_id, self.note_title, self.text)
        # log success

    def action_load_note(self) -> None:
        """Load note content to the widget."""
        self.text = load_notes()[1]["content"]  #TODO needs to be triggered by tree
        # log success

    def on_mount(self) -> None:
        self.border_title = "Details"
        self.text = "Select note to see the details"
        self.disabled = True

    def on_text_area_changed(self) -> None:
        pass  # for testing purposes, might use in future for example highlighting editing


class Sidebar(Tree, can_focus=True):
    """Sidebar widget."""

    def on_mount(self):
        self.show_root = False
        self.border_title = "Notes"
        gen = self.root.add("General", expand=True)
        for note in load_notes():
            gen.add_leaf(note["title"] + " - " + note["created"], data=note)

    def on_focus(self) -> None:
        # self.border_subtitle = "Active"
        self.clear()
        gen = self.root.add("General", expand=True)
        for note in load_notes():
            gen.add_leaf(note["title"] + " - " + note["created"], data=note)


class Stats(Static, can_focus=False):
    """Stats and or To-Do."""
    def on_mount(self) -> None:
        self.border_title = "Stats"