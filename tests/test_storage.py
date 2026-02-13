"""Tests for the storage module."""

import json
from pathlib import Path

import pytest

from tui_notes.storage import _get_data_dir, _get_data_file, load_notes, save_notes


@pytest.fixture
def tmp_data_dir(tmp_path, monkeypatch):
    """Override data dir to use a temporary directory."""
    monkeypatch.setattr("tui_notes.storage._get_data_dir", lambda: tmp_path)
    monkeypatch.setattr("tui_notes.storage._get_data_file", lambda: tmp_path / "notes.json")
    return tmp_path


class TestSaveNotes:
    def test_save_creates_file(self, tmp_data_dir):
        save_notes([{"position": 0, "title": "Test", "content": "Hello"}])
        assert (tmp_data_dir / "notes.json").exists()

    def test_save_valid_json(self, tmp_data_dir):
        notes = [{"position": 0, "title": "A", "content": "B", "color_index": 2}]
        save_notes(notes)
        data = json.loads((tmp_data_dir / "notes.json").read_text())
        assert data["version"] == "1.0"
        assert data["post_its"] == notes

    def test_save_multiple_notes(self, tmp_data_dir):
        notes = [
            {"position": 0, "title": "Note 1", "content": "First"},
            {"position": 4, "title": "Note 2", "content": "Second"},
            {"position": 8, "title": "Note 3", "content": "Third"},
        ]
        save_notes(notes)
        data = json.loads((tmp_data_dir / "notes.json").read_text())
        assert len(data["post_its"]) == 3

    def test_save_empty_list(self, tmp_data_dir):
        save_notes([])
        data = json.loads((tmp_data_dir / "notes.json").read_text())
        assert data["post_its"] == []

    def test_save_overwrites_existing(self, tmp_data_dir):
        save_notes([{"position": 0, "title": "Old", "content": ""}])
        save_notes([{"position": 0, "title": "New", "content": ""}])
        data = json.loads((tmp_data_dir / "notes.json").read_text())
        assert data["post_its"][0]["title"] == "New"

    def test_save_unicode(self, tmp_data_dir):
        save_notes([{"position": 0, "title": "Nota 📝", "content": "Conteúdo com acentuação"}])
        data = json.loads((tmp_data_dir / "notes.json").read_text(encoding="utf-8"))
        assert data["post_its"][0]["title"] == "Nota 📝"


class TestLoadNotes:
    def test_load_nonexistent_returns_empty(self, tmp_data_dir):
        assert load_notes() == []

    def test_load_saved_notes(self, tmp_data_dir):
        notes = [{"position": 0, "title": "Test", "content": "Hello"}]
        save_notes(notes)
        loaded = load_notes()
        assert len(loaded) == 1
        assert loaded[0]["title"] == "Test"
        assert loaded[0]["content"] == "Hello"
        assert loaded[0]["position"] == 0

    def test_load_preserves_color_index(self, tmp_data_dir):
        save_notes([{"position": 0, "title": "T", "content": "", "color_index": 3}])
        loaded = load_notes()
        assert loaded[0]["color_index"] == 3

    def test_load_default_color_index(self, tmp_data_dir):
        """Notes without color_index get default based on position."""
        raw = {"version": "1.0", "post_its": [{"position": 2, "title": "T"}]}
        (tmp_data_dir / "notes.json").write_text(json.dumps(raw))
        loaded = load_notes()
        assert loaded[0]["color_index"] == 2  # position % 6

    def test_load_invalid_json_returns_empty(self, tmp_data_dir):
        (tmp_data_dir / "notes.json").write_text("not json at all")
        assert load_notes() == []

    def test_load_wrong_structure_returns_empty(self, tmp_data_dir):
        (tmp_data_dir / "notes.json").write_text(json.dumps({"wrong": "data"}))
        assert load_notes() == []

    def test_load_filters_invalid_notes(self, tmp_data_dir):
        raw = {
            "version": "1.0",
            "post_its": [
                {"position": 0, "title": "Valid"},
                {"bad": "note"},
                {"position": 1},  # missing title
                {"position": 2, "title": "Also valid"},
            ],
        }
        (tmp_data_dir / "notes.json").write_text(json.dumps(raw))
        loaded = load_notes()
        assert len(loaded) == 2
        assert loaded[0]["title"] == "Valid"
        assert loaded[1]["title"] == "Also valid"

    def test_load_roundtrip(self, tmp_data_dir):
        """Save and load should preserve all data."""
        original = [
            {"position": 0, "title": "Note 1", "content": "Content 1", "color_index": 0},
            {"position": 5, "title": "Note 2", "content": "Content 2", "color_index": 4},
        ]
        save_notes(original)
        loaded = load_notes()
        assert loaded == original


class TestDataDir:
    def test_get_data_dir_returns_path(self):
        result = _get_data_dir()
        assert isinstance(result, Path)
        assert result.name == "tui-notes"

    def test_get_data_file_returns_json(self):
        result = _get_data_file()
        assert result.name == "notes.json"
        assert result.parent.name == "tui-notes"
