from textual.reactive import reactive
from textual.widgets import TextArea

from utils import update_note_content


class Content(TextArea):
    """Note content widget."""

    BINDINGS = [
        ("ctrl+s", "save_note", "Save Note"),
    ]

    note_id = reactive(None)

    def load_data(self, data: object) -> None:
        """Load note content to the widget."""
        try:
            self.note_id = data[0]
            self.text = data[2]
        except TypeError:
            #self.border_title = str(data)  #TODO: something better in here
            self.disabled = True

    def action_save_note(self) -> None:
        """Save note content to DB."""
        update_note_content(self.note_id, self.text)
        self.border_title = "Saved"
        # log success

    def on_focus(self) -> None:
        self.disabled = False

    def on_mount(self) -> None:
        self.border_title = "Content"

    def on_text_area_changed(self) -> None:
        if self.has_focus:
            self.border_title = "Content - Edited"
