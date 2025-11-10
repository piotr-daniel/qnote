from textual.containers import Grid
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static, TextArea, Tree, Input
from textual.widgets.tree import TreeNode
from utils import add_note, delete_note, get_categories, get_notes, update_note


class Details(TextArea):
    """Note details widget."""

    BINDINGS = [
        ("ctrl+s", "save_note", "Save Note"),
        ("ctrl+l", "add_note", "Add New Note"),
    ]

    note_id = reactive(None)
    note_title = reactive(None)

    def load_data(self, data: object) -> None:
        """Load note content to the widget."""
        try:
            self.note_id = data[0]
            self.note_title = data[1]
            self.text = data[2]
        except TypeError as e:
            self.border_title = "Empty Loaded"

    def action_add_note(self) -> None:
        add_note("", self.text)

    def action_save_note(self) -> None:
        """Save note content to DB."""
        update_note(self.note_id, self.text)
        self.border_title = "Saved"
        # log success

    def on_mount(self) -> None:
        self.border_title = "Details"

    def on_text_area_changed(self) -> None:
        # self.border_title = "Details - Edited"
        pass


class Sidebar(Tree, can_focus=True):
    """Sidebar widget."""

    BINDINGS = [
        ("ctrl+a", "new_note", "New"),
        ("ctrl+delete", "delete_note", "Delete"),
    ]

    def update_tree(self):  #TODO: add categories from db
        # gen = self.root.add("General", expand=True)
        categories = get_categories()[0]
        for category in categories:
            cat = self.root.add(category, expand=True)
            for note in get_notes():
                note_title = note[1]
                cat.add_leaf(note_title + " - " + note[5], data=note)

    def action_new_note(self) -> None:
        add_note("New Note", "")
        self.clear()
        self.update_tree()
        self.move_cursor_to_line(1)
        self.screen.focus_next()

    def action_delete_note(self) -> None:  #TODO: confirmation dialog
        if str(self.NodeHighlighted(self.cursor_node).node.label) != "General":
            delete_note(self.NodeHighlighted(self.cursor_node).node.data[0])
            self.clear()
            self.update_tree()

    def on_mount(self):
        self.show_root = False
        self.border_title = "Notes"
        self.update_tree()

    def on_focus(self) -> None:
        self.clear()
        self.update_tree()


class Stats(Static, can_focus=False):
    """Stats and or To-Do."""
    def on_mount(self) -> None:
        self.border_title = "Stats"
        self.content = str(get_notes())
