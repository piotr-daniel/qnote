from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header

from . import themes
from .utils import init_db
from .widgets.content import Content
from .widgets.sidebar import Sidebar
from .widgets.stats import Stats


class QnoteApp(App):
    """A Textual app to easily take and manage notes."""

    AUTO_FOCUS = "#sidebar"
    CSS_PATH = "default.tcss"
    TITLE = "QNote"
    BINDINGS = [
        #("d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+l", "toggle_lumen_off", "Lumen Off"),
        ("ctrl+l", "toggle_lumen_on", "Lumen On")
    ]

    def on_mount(self):
        init_db()

        for theme in themes.all_themes:
            self.register_theme(theme)
        self.theme = "qnote"


    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()
        yield Footer()

        with Horizontal():
            with VerticalScroll(classes="column", id="left-pane", can_focus=False):
                yield Sidebar("Notes", id="sidebar")
            with Vertical(classes="column", id="right-pane"):
                yield Stats(id="stats")
                yield Content(classes="inactive", id="content")


    def on_tree_node_highlighted(self, node) -> None:
        """Show details of note highlighted note."""

        content = self.query_one(Content)
        content_input = self.query_one("#content-input")

        if not node.node.children:
            try:
                content.border_title = "Content"
                content.load_data(node.node)
                self.query_one(Stats).load_data(node.node.data)
            except (AttributeError, TypeError) as e:
                content.text = str(e)
            else:
                pass
        else:
            if not content_input.has_focus:
                content_input.text = str(node.node.label)
                content.disabled = True

            self.query_one(Stats).load_data(node.node)


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = "gruvbox" if self.theme == "qnote" else "qnote"


    def action_toggle_lumen_off(self) -> None:
        """An action to toggle lumen mode."""
        self.query_one(Stats).lumen_active = False
        self.query_one("#lumen").visible = False


    def action_toggle_lumen_on(self) -> None:
        """An action to toggle lumen mode."""
        self.query_one(Stats).lumen_active = True
        self.query_one("#lumen").visible = True


    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action may run."""
        if action == "toggle_lumen_off" and not self.query_one(Stats).lumen_active:
            return False
        return True


if __name__ == "__main__":
    app = QnoteApp()
    app.run()
