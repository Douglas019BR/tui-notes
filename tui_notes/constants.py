"""Shared constants for tui-notes."""

MAX_NOTES: int = 9
"""Maximum number of post-its in the grid."""

GRID_COLUMNS: int = 3
"""Number of columns in the grid layout."""

COLORS: list[tuple[str, str]] = [
    ("Yellow", "post-it-0"),
    ("Green", "post-it-1"),
    ("Blue", "post-it-2"),
    ("Pink", "post-it-3"),
    ("Orange", "post-it-4"),
    ("Purple", "post-it-5"),
]
"""Available post-it colors as (display_name, css_class) tuples."""

NUM_COLORS: int = len(COLORS)
"""Total number of available colors."""
