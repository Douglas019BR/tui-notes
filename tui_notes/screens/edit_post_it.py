"""Edit post-it modal screen."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Static, TextArea


class EditPostItScreen(ModalScreen[dict | None]):
    """Modal screen for editing a post-it note's title and content."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, title: str, content: str) -> None:
        """Initialize with the current note values.

        Args:
            title: Current note title.
            content: Current note content.
        """
        super().__init__()
        self._edit_title = title
        self._edit_content = content

    def compose(self) -> ComposeResult:
        """Compose the edit modal layout."""
        with Container(id="edit-modal"):
            yield Static("Edit Note", id="edit-modal-title")
            yield Input(value=self._edit_title, placeholder="Title", id="edit-title-input")
            yield TextArea(self._edit_content, id="edit-content-input")
            with Horizontal(id="edit-buttons"):
                yield Button("Save", variant="primary", id="edit-save")
                yield Button("Cancel", variant="default", id="edit-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle Save or Cancel button clicks."""
        if event.button.id == "edit-save":
            title = self.query_one("#edit-title-input", Input).value
            content = self.query_one("#edit-content-input", TextArea).text
            self.dismiss({"title": title, "content": content})
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        """Dismiss the modal without saving."""
        self.dismiss(None)
