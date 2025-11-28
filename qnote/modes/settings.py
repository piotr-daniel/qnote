from textual.app import ComposeResult
from textual.screen import ModalScreen, Screen
from textual.widgets import Footer, Placeholder


class SettingsScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Placeholder("Settings Screen")
        yield Footer()