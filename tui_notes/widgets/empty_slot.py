"""Empty slot placeholder widget."""

from textual.widgets import Static


class EmptySlot(Static, can_focus=True):
    """Placeholder widget for an empty position in the post-it grid."""

    def __init__(self, **kwargs: object) -> None:
        """Initialize an empty slot with placeholder text.

        Args:
            **kwargs: Additional keyword arguments passed to Static.
        """
        super().__init__("Press 'a' to add a note", **kwargs)
        self.add_class("empty-slot")
