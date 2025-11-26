from datetime import datetime
from textual.app import ComposeResult
from textual.containers import Grid
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Tree

from ..utils import (
    add_note,
    delete_note,
    get_categories,
    get_notes,
)


class Sidebar(Tree, can_focus=True):
    """Sidebar widget."""

    BINDINGS = [
        ("ctrl+n", "new_note", "New"),
        ("ctrl+e", "edit_content", "Edit"),
        ("ctrl+delete", "check_delete_note", "Delete"),
    ]

    def on_mount(self):
        self.show_root = False
        self.guide_depth = 3
        self.border_title = "Notes"
        self.update_tree()
        self.move_cursor_to_line(0)

    def on_focus(self) -> None:
        self.screen.query_one("Content").disabled = True
        self.screen.query_one("Content").add_class("inactive")
        self.update_tree()

    def update_tree(self):
        self.clear()
        categories = get_categories()
        for category in categories:
            cat = self.root.add(category, expand=True)
            for note in get_notes():
                if note[3] == category:
                    cat.add_leaf(
                        f"{note[1]}{' ' * (45-len(note[1]))} [{datetime.strptime(note[6], "%Y-%m-%d %H:%M:%S").date()}]",
                        data={
                            "id": note[0],
                            "title": note[1],
                            "content": note[2],
                            "category": note[3],
                            "tags": note[4],
                            "created": datetime.strptime(note[5], "%Y-%m-%d %H:%M:%S"),
                            "updated": datetime.strptime(note[6], "%Y-%m-%d %H:%M:%S"),
                        },
                    )

    def action_new_note(self) -> None:
        """Create a new note."""

        category = ""
        new_line = reactive(0)

        if self.cursor_node.parent == self.root:
            category = str(self.cursor_node.label)
            new_line = self.cursor_line + 1
        else:
            category = str(self.cursor_node.parent.label)
            new_line = self.cursor_node.parent.line + 1

        add_note("New Note", "", category)
        self.update_tree()

        # Trigger on_highlight action
        self.select_node(None)
        self.move_cursor_to_line(new_line)

        # Move focus and cursor to the content text area for instant access
        self.screen.query_one("Content").disabled = False
        self.screen.query_one("#content-input").disabled = False
        self.screen.focus_next("#content-input")
        self.can_focus = False

    def action_delete_note(self) -> None:
        has_children = len(self.cursor_node.children) > 0
        note_id = self.NodeHighlighted(self.cursor_node).node.data["id"]
        cursor_line = self.cursor_line
        if not has_children:
            delete_note(note_id)
            self.update_tree()
            self.select_node(None)
            self.move_cursor_to_line(cursor_line-1)
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

    def action_edit_content(self) -> None:
        has_children = len(self.cursor_node.children) > 0

        if not has_children:
            self.app.query_one("#stats").is_animating = True
            self.screen.query_one("Content").disabled = False
            self.screen.query_one("#title-input").disabled = False
            self.screen.query_one("#category-input").disabled = False
            self.screen.query_one("#content-input").disabled = False
            self.screen.focus_next("#content-input")
            self.can_focus = False


class DeleteScreen(ModalScreen[bool]):
    """Screen with a dialog to confirm delete note."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to delete?", id="question"),
            Button("Yes, Delete", variant="error", id="confirm-delete"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm-delete":
            self.dismiss(True)
        else:
            self.dismiss(False)
