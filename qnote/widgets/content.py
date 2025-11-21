import asyncio
from random import randint
from time import sleep

from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Label, TextArea

from utils import update_note_content, update_note_category, update_note_title


class ContentInput(TextArea):
    """Note content widget."""

    def on_focus(self) -> None:
        self.parent.remove_class("inactive")
        self.action_cursor_line_end()
        self.action_cursor_page_down()

    def on_text_area_changed(self) -> None:
        if self.has_focus:
            self.parent.border_title = "Content - Edited"
            letters = ["a", "p", "f", "o"]
            self.app.query_one("#stats").vis.content = letters[randint(0, len(letters) - 1)]


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
        with HorizontalGroup(id="content_header"):
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

        # log success
        update_note_title(self.note_id, self.title_input.value)
        update_note_category(self.note_id, self.category_input.value)
        self.app.query_one("#sidebar").can_focus = True
        self.app.query_one("#sidebar").update_tree()
        self.screen.focus_next("#sidebar").refresh()
        new_line = self.app.query_one("#sidebar").cursor_node.parent.line + 1
        self.app.query_one("#sidebar").select_node(None)
        self.app.query_one("#sidebar").move_cursor_to_line(new_line)
        self.call_later(self.save_confirm_visual)


    async def save_confirm_visual(self):
        """Add a visual cue that note is saved."""

        self.add_class("saved")
        self.border_title = "Saved"
        await asyncio.sleep(1)
        self.border_title = "Content"
        self.remove_class("saved")
        self.refresh()
        self.disabled = True
        #self.styles.animate("opacity ", value=1, duration=2.0)


    def action_cancel_edit(self) -> None:
        """Cancel edit."""

        self.border_title = "Content"
        self.app.query_one("#sidebar").can_focus = True
        self.screen.focus_next("#sidebar")
        node_line = self.app.query_one("#sidebar").cursor_node.line
        self.app.query_one("#sidebar").select_node(None)
        self.app.query_one("#sidebar").move_cursor_to_line(node_line)
        self.app.query_one("Content").disabled = True


    def on_focus(self) -> None:
        self.disabled = False


    def on_mount(self) -> None:
        self.border_title = "Content"


    def on_input_submitted(self):  #keeping for ref
        """Submit title and category."""
        pass

        #update_note_title(self.note_id, self.title_input.value)
        #update_note_category(self.note_id, self.category_input.value)
        #self.title_input.disabled = True
        #self.category_input.disabled = True
        #self.content_input.disabled = True
        #self.disabled = True
        #self.app.query_one("#sidebar").can_focus = True
        #self.screen.focus_next("#sidebar").refresh()
