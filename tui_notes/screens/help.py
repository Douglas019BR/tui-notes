"""Help modal screen."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Static


class HelpScreen(ModalScreen[None]):
    """Modal screen showing all keyboard shortcuts."""

    BINDINGS = [
        Binding("escape", "close", "Close"),
        Binding("question_mark", "close", "Close", show=False),
    ]

    HELP_TEXT = """\
╔══════════════════════════════════════╗
║         TUI Notes - Help             ║
╠══════════════════════════════════════╣
║                                      ║
║  Navigation                          ║
║  ← ↑ ↓ →    Move between slots       ║
║                                      ║
║  Notes                               ║
║  a          Add note at position     ║
║  e / Enter  Edit selected note       ║
║  d          Delete selected note     ║
║  c          Change note color        ║
║                                      ║
║  Organization                        ║
║  m          Move mode (swap notes)   ║
║  Escape     Cancel move mode         ║
║                                      ║
║  File                                ║
║  Ctrl+S     Save notes               ║
║  Ctrl+R     Reload notes             ║
║  Ctrl+E     Export to markdown       ║
║                                      ║
║  Other                               ║
║  ?          Show this help           ║
║  q          Quit                     ║
║                                      ║
╚══════════════════════════════════════╝\
"""

    def compose(self) -> ComposeResult:
        """Compose the help screen layout."""
        with Container(id="help-modal"):
            yield Static(self.HELP_TEXT, id="help-text")
            yield Static("Press Escape or ? to close", id="help-close-hint")

    def action_close(self) -> None:
        """Dismiss the help screen."""
        self.dismiss(None)

    def on_key(self, event: Key) -> None:
        """Dismiss on any key press."""
        self.dismiss(None)
