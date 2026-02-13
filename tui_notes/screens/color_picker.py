"""Color picker modal screen."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Static

from tui_notes.constants import COLORS


class ColorPickerScreen(ModalScreen[int | None]):
    """Modal screen for selecting a post-it color from the palette."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the color picker layout with one button per color."""
        with Container(id="color-modal"):
            yield Static("Choose a color", id="color-modal-title")
            with Horizontal(id="color-options"):
                for i, (name, css_class) in enumerate(COLORS):
                    yield Button(name, id=f"color-{i}", classes=f"color-btn {css_class}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Dismiss with the selected color index."""
        btn_id = event.button.id or ""
        if btn_id.startswith("color-"):
            idx = int(btn_id.split("-")[1])
            self.dismiss(idx)

    def action_cancel(self) -> None:
        """Dismiss without selecting a color."""
        self.dismiss(None)
