from idlelib.tree import TreeNode
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header

from utils import init_db
from widgets.content import Content
from widgets.stats import Stats
from widgets.sidebar import Sidebar


class QnoteApp(App):
    """A Textual app to easily take and manage notes."""

    init_db()

    AUTO_FOCUS = "#sidebar"
    CSS_PATH = "default.tcss"
    TITLE = "QNote"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+q", "quit", "Quit"),
    ]

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


    def on_tree_node_highlighted(self, node:TreeNode) -> None:
        """Show details of note highlighted note."""

        if not node.node.children:
            try:
                self.query_one(Content).border_title = "Content"
                self.query_one(Content).load_data(node.node)
                self.query_one(Stats).load_data(node.node.data)
            except (AttributeError, TypeError) as e:
                self.query_one(Content).text = str(e)
                #TODO: add logging here
            else:
                pass
        else:
            if not self.query_one("#content-input").has_focus:
                self.query_one("#content-input").text = str(node.node.label)
                self.query_one(Content).disabled = True

            self.query_one(Stats).load_data(node.node)


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = QnoteApp()
    app.run()