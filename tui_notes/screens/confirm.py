"""Confirmation modal screen."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class ConfirmScreen(ModalScreen[bool]):
    """Modal screen that asks for yes/no confirmation."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, message: str) -> None:
        """Initialize with a confirmation message.

        Args:
            message: The question to display.
        """
        super().__init__()
        self._message = message

    def compose(self) -> ComposeResult:
        """Compose the confirmation dialog layout."""
        with Container(id="confirm-modal"):
            yield Static(self._message, id="confirm-message")
            with Horizontal(id="confirm-buttons"):
                yield Button("Yes", variant="error", id="confirm-yes")
                yield Button("No", variant="default", id="confirm-no")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Dismiss with True for Yes, False for No."""
        self.dismiss(event.button.id == "confirm-yes")

    def action_cancel(self) -> None:
        """Dismiss as cancelled (False)."""
        self.dismiss(False)
