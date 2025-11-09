from idlelib.tree import TreeNode
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header
from utils import init_db, get_notes
from widgets import Details, Sidebar, Stats


class QnoteApp(App):
    """A Textual app to easily take and manage notes."""

    init_db()

    CSS_PATH = "default.tcss"
    TITLE = "QNote"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header()
        yield Footer()

        with Horizontal():
            with VerticalScroll(classes="column", id="left-pane"):
                yield Sidebar("Notes")
            with Vertical(classes="column", id="right-pane"):
                yield Stats()
                yield Details()


    def on_tree_node_highlighted(self, node:TreeNode) -> None:
        if not node.node.children:
            self.query_one(Details).disabled = False
            self.query_one(Details).load_data(node.node.data)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = QnoteApp()
    app.run()