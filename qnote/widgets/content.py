from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Label, TextArea

from utils import update_note_content, update_note_category, update_note_title


class ContentInput(TextArea):
    """Note content widget."""

    def on_focus(self) -> None:
        self.action_cursor_line_end()
        self.action_cursor_page_down()

    def on_text_area_changed(self) -> None:
        if self.has_focus:
            self.parent.border_title = "Content - Edited"


class Content(Widget):
    """Note content container."""

    BINDINGS = [
        ("ctrl+s", "save_note", "Save Note"),
        ("ctrl+delete", "cancel_edit", "Cancel"),
    ]

    title_input = Input(id="title_input", compact=True, disabled=True)
    category_input = Input(id="category_input", compact=True, disabled=True)
    content_input = ContentInput(id="content_input", disabled=True)

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label("Title: ")
            yield self.title_input
            yield Label("Category: ")
            yield self.category_input
        yield self.content_input

    note_id = reactive(None)

    def load_data(self, data: object) -> None:
        """Load note content to the widget."""
        try:
            self.note_id = data[0]
            self.title_input.value = data[1]
            self.category_input.value = data[3]
            self.content_input.text = data[2]
        except TypeError:
            #self.border_title = str(data)  #TODO: something better in here
            #self.disabled = True
            pass

    def action_save_note(self) -> None:
        """Save note content to DB."""

        update_note_content(self.note_id, self.content_input.text)
        self.border_title = "Saved"
        # log success
        update_note_title(self.note_id, self.title_input.value)
        update_note_category(self.note_id, self.category_input.value)
        self.title_input.disabled = True
        self.category_input.disabled = True
        self.content_input.disabled = True
        self.disabled = True
        self.app.query_one("#sidebar").can_focus = True
        self.screen.focus_next("#sidebar").refresh()

    def action_cancel_edit(self) -> None:
        """Cancel edit."""

        self.app.query_one("#sidebar").can_focus = True
        self.screen.focus_next("#sidebar")
        self.app.query_one("Content").disabled = True

    def on_focus(self) -> None:
        self.disabled = False

    def on_mount(self) -> None:
        self.border_title = "Content"

    def on_input_submitted(self):  #TODO: this to work on next
        """Submit title and category."""

        update_note_title(self.note_id, self.title_input.value)
        update_note_category(self.note_id, self.category_input.value)
        self.title_input.disabled = True
        self.category_input.disabled = True
        self.content_input.disabled = True
        self.disabled = True
        self.app.query_one("#sidebar").can_focus = True
        self.screen.focus_next("#sidebar").refresh()
