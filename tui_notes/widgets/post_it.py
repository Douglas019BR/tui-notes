"""Post-it note widget."""

from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Static

from tui_notes.constants import NUM_COLORS


class PostIt(Container, can_focus=True):
    """A single post-it note widget with reactive title, content, and color."""

    title: reactive[str] = reactive("")
    content: reactive[str] = reactive("")
    position: reactive[int] = reactive(0)
    color_index: reactive[int] = reactive(0)

    def __init__(
        self,
        position: int,
        title: str = "",
        content: str = "",
        color_index: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize a post-it note.

        Args:
            position: Grid position index (0-8).
            title: Note title. Defaults to 'Note {position + 1}'.
            content: Note body text.
            color_index: Color palette index (0-5). Defaults to position % 6.
            **kwargs: Additional keyword arguments passed to Container.
        """
        super().__init__(**kwargs)
        self.position = position
        self.title = title or f"Note {position + 1}"
        self.content = content
        self.color_index = color_index if color_index is not None else position % NUM_COLORS
        self.add_class(f"post-it-{self.color_index}")

    def compose(self) -> ComposeResult:
        """Compose the post-it layout with title and content labels."""
        yield Static(self.title, classes="post-it-title")
        yield Static(self.content or "( empty )", classes="post-it-content")

    def watch_title(self, new_title: str) -> None:
        """Update the title label when the reactive property changes."""
        try:
            self.query_one(".post-it-title", Static).update(new_title)
        except Exception:  # noqa: BLE001 - widget may not be composed yet
            pass

    def watch_content(self, new_content: str) -> None:
        """Update the content label when the reactive property changes."""
        try:
            self.query_one(".post-it-content", Static).update(new_content or "( empty )")
        except Exception:  # noqa: BLE001 - widget may not be composed yet
            pass

    def watch_color_index(self, new_color: int) -> None:
        """Swap CSS color class when the color index changes."""
        for i in range(NUM_COLORS):
            self.remove_class(f"post-it-{i}")
        self.add_class(f"post-it-{new_color}")

    def to_dict(self, grid_index: int | None = None) -> dict[str, Any]:
        """Serialize this post-it to a dictionary for persistence.

        Args:
            grid_index: Override position with actual grid index. If None, uses self.position.

        Returns:
            Dictionary with position, title, content, and color_index keys.
        """
        return {
            "position": grid_index if grid_index is not None else self.position,
            "title": self.title,
            "content": self.content,
            "color_index": self.color_index,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PostIt":
        """Create a PostIt instance from a persistence dictionary.

        Args:
            data: Dictionary with position, title, content, and optional color_index.

        Returns:
            A new PostIt instance.
        """
        return cls(
            position=data["position"],
            title=data["title"],
            content=data.get("content", ""),
            color_index=data.get("color_index"),
        )
