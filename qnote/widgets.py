from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.reactive import reactive
from textual.widgets import Button, Label, Static, TextArea, Tree
from utils import add_note, delete_note, get_categories, get_notes, update_note


class Details(TextArea):
    """Note details widget."""

    BINDINGS = [
        ("ctrl+s", "save_note", "Save Note"),
    ]

    note_id = reactive(None)
    note_title = reactive(None)

    def load_data(self, data: object) -> None:
        """Load note content to the widget."""
        try:
            self.note_id = data[0]
            self.note_title = data[1]
            self.text = data[2]
        except TypeError:
            self.border_title = "Empty Loaded"

    def action_save_note(self) -> None:
        """Save note content to DB."""
        update_note(self.note_id, self.text)
        self.border_title = "Saved"
        # log success

    def on_focus(self) -> None:
        self.disabled = False

    def on_mount(self) -> None:
        self.border_title = "Details"

    def on_text_area_changed(self) -> None:
        if self.has_focus:
            self.border_title = "Details - Edited"


class Sidebar(Tree, can_focus=True):
    """Sidebar widget."""

    BINDINGS = [
        ("ctrl+a", "new_note", "New"),
        ("ctrl+delete", "check_delete_note", "Delete"),
    ]

    def update_tree(self):
        self.clear()
        categories = get_categories()
        for category in categories:
            cat = self.root.add(category, expand=True)
            for note in get_notes():
                if note[3] == category:
                    note_title = note[1]
                    cat.add_leaf(note_title + " - " + note[5], data=note)

    def action_new_note(self) -> None:
        category = ""
        new_line = 0
        if self.cursor_node.parent == self.root:
            category = str(self.cursor_node.label)
            new_line = self.cursor_line + 1
        else:
            category = str(self.cursor_node.parent.label)
            new_line = self.cursor_node.parent.line + 1
        add_note("New Note", "", category)
        # self.clear()
        self.update_tree()
        self.move_cursor_to_line(new_line, True)
        self.app.query_one(Details).disabled = False
        self.screen.focus_next(Details)

    def action_delete_note(self) -> None:
        has_children = len(self.cursor_node.children) > 0
        if not has_children:
            delete_note(self.NodeHighlighted(self.cursor_node).node.data[0])
            # self.clear()
            self.update_tree()
            self.action_cursor_up()
            self.refresh()

    def action_check_delete_note(self) -> None:
        """Display the confirm delete dialog for note node."""

        def check_delete(delete: bool | None) -> None:
            if delete:
                self.action_delete_note()

        if self.cursor_node.parent == self.root:
            pass
        else:
            self.app.push_screen(DeleteScreen(), check_delete)

    def on_mount(self):
        self.show_root = False
        self.border_title = "Notes"
        # self.clear()
        self.update_tree()

    def on_focus(self) -> None:
        # self.clear()
        self.update_tree()


class DeleteScreen(ModalScreen[bool]):
    """Screen with a dialog to confirm delete note."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to delete?", id="question"),
            Button("Yes, Delete", variant="error", id="confirm_delete"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_delete":
            self.dismiss(True)
        else:
            self.dismiss(False)


class Stats(Static, can_focus=False):
    """Stats and or To-Do."""
    def on_mount(self) -> None:
        self.border_title = "Stats"
        self.content = str(get_notes())
