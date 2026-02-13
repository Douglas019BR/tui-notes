"""Persistence layer for tui-notes. Saves/loads post-its as JSON."""

import json
import os
import platform
from pathlib import Path
from typing import Any


def _get_data_dir() -> Path:
    """Return the platform-specific data directory for tui-notes.

    Returns:
        Path to the tui-notes configuration directory.
    """
    system = platform.system()
    if system == "Windows":
        base = Path.home() / "AppData" / "Roaming"
    elif system == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        base = Path(xdg_config) if xdg_config else Path.home() / ".config"
    return base / "tui-notes"


def _get_data_file() -> Path:
    """Return the path to the notes JSON file.

    Returns:
        Path to notes.json inside the data directory.
    """
    return _get_data_dir() / "notes.json"


def save_notes(post_its: list[dict[str, Any]]) -> None:
    """Save post-its to JSON file using atomic write.

    Writes to a temporary file first, then atomically replaces the
    target file to prevent data corruption on failures.

    Args:
        post_its: List of dicts with keys: position, title, content, color_index.

    Raises:
        OSError: If the file cannot be written.
    """
    data_dir = _get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)

    data = {"version": "1.0", "post_its": post_its}

    tmp_file = _get_data_file().with_suffix(".tmp")
    try:
        tmp_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_file.replace(_get_data_file())
    except OSError:
        tmp_file.unlink(missing_ok=True)
        raise


def _validate_note(note: Any) -> dict[str, Any] | None:
    """Validate and normalize a single note dictionary.

    Args:
        note: Raw note data from JSON.

    Returns:
        Normalized note dict, or None if invalid.
    """
    if not isinstance(note, dict):
        return None
    if "position" not in note or "title" not in note:
        return None
    return {
        "position": int(note["position"]),
        "title": str(note["title"]),
        "content": str(note.get("content", "")),
        "color_index": int(note.get("color_index", note["position"] % 6)),
    }


def load_notes() -> list[dict[str, Any]]:
    """Load post-its from JSON file.

    Returns:
        List of validated note dicts. Empty list if file doesn't
        exist, is corrupted, or contains no valid notes.
    """
    data_file = _get_data_file()
    if not data_file.exists():
        return []

    try:
        raw = data_file.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, dict) or "post_its" not in data:
            return []
        notes = data["post_its"]
        if not isinstance(notes, list):
            return []
        return [v for note in notes if (v := _validate_note(note)) is not None]
    except (json.JSONDecodeError, OSError, ValueError):
        return []
