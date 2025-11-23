import asyncio
from random import choice

from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Label, Rule, TextArea

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
            #self.app.query_one("#stats").vis.content = choice(letters)


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
        yield Rule()
        yield self.content_input


    note_id = reactive(None)
    node = None

    sidebar: Widget | None = None


    def load_data(self, node: object) -> None:
        """Load note content to the widget."""
        try:
            self.node = node
            self.note_id = node.data["id"]
            self.title_input.value = node.data["title"]
            self.category_input.value = node.data["category"]
            self.content_input.text = node.data["content"]
        except TypeError:
            #self.border_title = str(data)  #TODO: something better in here
            #self.disabled = True
            pass


    def on_mount(self) -> None:
        self.border_title = "Content"
        self.sidebar = self.app.query_one("#sidebar")


    def on_focus(self) -> None:
        self.disabled = False


    def action_save_note(self) -> None:
        """Save note content to DB."""

        update_note_content(self.note_id, self.content_input.text)
        update_note_title(self.note_id, self.title_input.value)
        update_note_category(self.note_id, self.category_input.value)

        self.sidebar.can_focus = True
        self.sidebar.update_tree()
        self.screen.focus_next("#sidebar").refresh()

        self.call_later(self._reselect)
        self.call_later(self._save_confirm_visual)

        self.app.query_one("#stats").is_animating = False


    async def _save_confirm_visual(self):
        """Add a visual cue that note is saved."""

        self.add_class("saved")
        self.border_title = "Saved"
        await asyncio.sleep(1)
        self.border_title = "Content"
        self.remove_class("saved")
        self.refresh()
        self.disabled = True
        #self.styles.animate("opacity ", value=1, duration=2.0)

    def _reselect(self):
        target_id = self.note_id

        def find_node(node):
            if getattr(node, "data", None) and node.data.get("id") == target_id:
                return node
            for child in getattr(node, "children", []):
                found = find_node(child)
                if found:
                    return found
            return None

        node = find_node(self.sidebar.root)
        if node:
            self.sidebar.select_node(node)
            self.sidebar.move_cursor(node)


    def action_cancel_edit(self) -> None:
        """Cancel edit."""

        self.border_title = "Content"
        self.sidebar.can_focus = True
        self.screen.focus_next("#sidebar")
        node_line = self.sidebar.cursor_node.line
        self.sidebar.select_node(None)
        self.sidebar.move_cursor_to_line(node_line)
        self.disabled = True
