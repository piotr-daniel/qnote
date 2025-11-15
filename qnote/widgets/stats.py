from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Label

from utils import get_notes, update_note_category, update_note_title


class Stats(Widget, can_focus=False):
    """Stats and or To-Do."""

    title_input = Input(id="title_input", compact=True, disabled=True)
    category_input = Input(id="category_input", compact=True, disabled=True)

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label("Title:")
            yield self.title_input
        with HorizontalGroup():
            yield Label("Category:")
            yield self.category_input

    note_id = reactive(None)

    def load_data(self, data: object) -> None:
        """Load note content to the widget."""
        try:
            self.note_id = data[0]
            self.title_input.value = data[1]
            self.category_input.value = data[3]
        except TypeError:
            self.title_input.value = ""
            self.category_input.value = ""
            # self.border_title = str(data)  # TODO: something better in here
            # self.disabled = True

    def on_mount(self) -> None:
        self.border_title = "Stats"
        self.disabled = False

    def on_input_submitted(self):  #TODO: this to work on next
        """Submit title and category."""

        update_note_title(self.note_id, self.title_input.value)
        update_note_category(self.note_id, self.category_input.value)
        self.screen.focus_next("#sidebar").refresh()