"""Main application module for tui-notes."""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Grid


class PostIt(Static):
    """A single post-it note widget."""

    def __init__(self, position: int, title: str = "", content: str = "") -> None:
        super().__init__()
        self.position = position
        self.note_title = title
        self.note_content = content

    def compose(self) -> ComposeResult:
        """Compose the post-it widget."""
        title = self.note_title or f"Note {self.position + 1}"
        content = self.note_content or "Empty"
        yield Static(f"[b]{title}[/b]\n\n{content}", classes="post-it-content")


class NotesApp(App):
    """A TUI application for managing post-it notes in a 3x3 grid."""

    CSS_PATH = "style.tcss"
    TITLE = "TUI Notes"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("?", "help", "Help"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header()
        yield Grid(
            *[PostIt(i) for i in range(9)],
            id="notes-grid",
        )
        yield Footer()

    def action_help(self) -> None:
        """Show help information."""
        self.notify("Press 'q' to quit. More features coming soon!")
