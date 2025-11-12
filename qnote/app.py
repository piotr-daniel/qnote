from idlelib.tree import TreeNode
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header
from utils import init_db, get_notes, add_note
from widgets import Details, Sidebar, Stats


class QnoteApp(App):
    """A Textual app to easily take and manage notes."""

    init_db()

    AUTO_FOCUS = "#sidebar"
    CSS_PATH = "default.tcss"
    TITLE = "QNote"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()
        yield Footer()

        with Horizontal():
            with VerticalScroll(classes="column", id="left-pane", can_focus=False):
                yield Sidebar("Notes", id="sidebar")
            with Vertical(classes="column", id="right-pane"):
                yield Stats()
                yield Details()


    def on_tree_node_highlighted(self, node:TreeNode) -> None:
        """Show details of note highlighted note."""
        if not node.node.children:
            try:
                self.query_one(Details).disabled = False
                self.query_one(Details).load_data(node.node.data)
            except AttributeError as e:
                self.query_one(Details).text = "parent empty"
                #TODO: add logging here
        else:
            if not self.query_one(Details).has_focus:
                self.query_one(Details).disabled = True
            self.query_one(Details).text = ""


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = QnoteApp()
    app.run()