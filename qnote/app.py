from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, HorizontalGroup, VerticalScroll, VerticalGroup
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Button, Digits, Footer, Header, Input, Static, Tree
from widgets.widgets import Details, Sidebar


class QnoteApp(App):
    """A Textual app to easily take and manage notes."""

    CSS_PATH = "default.tcss"
    TITLE = "QNote"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with Horizontal():
            with VerticalScroll(classes="column", id="left-pane"):
                yield Sidebar()
            with Vertical(classes="column", id="right-pane"):
                yield Stats()
                yield Details()

        # yield TextArea("Test text")
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = QnoteApp()
    app.run()