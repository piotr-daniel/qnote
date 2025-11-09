from textual.containers import Grid
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Label, Static, TextArea, Tree
from textual.widgets.tree import TreeNode
from utils import add_note, delete_note, get_notes, update_note


class Details(TextArea):
    """Note details widget."""

    BINDINGS = [
        ("ctrl+s", "save_note()", "Save Note"),
        ("ctrl+l", "add_note()", "Add New Note"),
    ]

    note_id = reactive(None)
    note_title = reactive(None)

    def load_data(self, data: object) -> None:
        """Load note content to the widget."""
        self.note_id = data[0]
        self.note_title = data[2][:20] if data[1] is None else data[1]
        self.text = data[2]

    def action_add_note(self) -> None:
        add_note("Testing sqlite", self.text)

    def action_save_note(self) -> None:  #TODO needs to save edited note and new func for adding
        """Save note content to DB."""
        update_note(self.note_id, self.text)
        # log success

    def on_mount(self) -> None:
        self.border_title = "Details"
        self.text = "Select note to see the details"
        self.disabled = True

    def on_text_area_changed(self) -> None:
        # self.border_title = "Details - Edited"
        pass


class Sidebar(Tree, can_focus=True):
    """Sidebar widget."""

    BINDINGS = [
        ("ctrl+delete", "delete_note()", "Delete Note"),
    ]

    def update_tree(self):
        # self.clear()
        gen = self.root.add("General", expand=True)
        for note in get_notes():
            note_title = note[2][:20] if note[1] is None else note[1]
            gen.add_leaf(note_title + " - " + note[4], data=note)

    def action_delete_note(self) -> None:
        self.app.push_screen(QuitScreen())
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


class DeleteScreen(Screen):
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to delete?", id="question"),
            Button("Yes, Delete", variant="error", id="delete"),
            Button("No, Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete":
            self.app.exit()
        else:
            self.app.pop_screen()