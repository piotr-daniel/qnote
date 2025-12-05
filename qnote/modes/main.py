from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header


from ..utils import get_setting
from ..widgets.content import Content
from ..widgets.sidebar import Sidebar, Search
from ..widgets.stats import Stats


class MainScreen(Screen):

    BINDINGS = [
        ("/", "search_note", "Search"),
        ("f12", "app.switch_mode('settings')", "Settings"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        yield Header(icon="")
        yield Footer()

        with Horizontal():
            with VerticalScroll(classes="column", id="left-pane", can_focus=False):
                yield Search(id="search", placeholder="Type / to Search...")
                yield Sidebar("Notes", id="sidebar")

            with Vertical(classes="column", id="right-pane"):
                yield Stats(id="stats")
                yield Content(classes="inactive", id="content")


    def on_tree_node_highlighted(self, node) -> None:
        """Show details of note highlighted note."""

        content = self.screen.query_one("Content")
        content_input = self.screen.query_one("#content-input")
        category_input = self.screen.query_one("#category-input")
        title_input = self.screen.query_one("#title-input")


        if not node.node.children:
            try:
                content.border_title = "Content"
                content.load_data(node.node)
                self.screen.query_one("Stats").load_data(node.node.data)
            except (AttributeError, TypeError) as e:
                content_input.text = str(e)
            else:
                pass
        else:
            if not content_input.has_focus:
                content_input.text = ""
                category_input.value = ""
                title_input.value = ""
                content.disabled = True

            self.screen.query_one("Stats").load_data(node.node)


    def action_search_note(self) -> None:
        self.screen.focus_next("#search")


    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action may run."""
        if action == "search_note" and (self.screen.query_one("#content-input").has_focus or self.screen.query_one("#search").has_focus):
            return False
        return True


    def _on_screen_resume(self):  #TODO: changing settings
        self.query_one(Stats).lumen.play_animation(get_setting("lumen"))
