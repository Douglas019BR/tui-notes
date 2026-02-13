"""Tests for the TUI Notes app using Textual's async testing."""

import pytest
from textual.pilot import Pilot

from tui_notes.app import NotesApp
from tui_notes.widgets import EmptySlot, PostIt


@pytest.fixture
def app(tmp_path, monkeypatch):
    """Create app with isolated storage."""
    monkeypatch.setattr("tui_notes.storage._get_data_dir", lambda: tmp_path)
    monkeypatch.setattr("tui_notes.storage._get_data_file", lambda: tmp_path / "notes.json")
    monkeypatch.setattr("tui_notes.app.load_notes", lambda: [])
    return NotesApp()


class TestAppStartup:
    @pytest.mark.asyncio
    async def test_app_starts_with_empty_grid(self, app):
        async with app.run_test() as pilot:
            post_its = app.query("PostIt")
            empty_slots = app.query("EmptySlot")
            assert len(post_its) == 0
            assert len(empty_slots) == 9

    @pytest.mark.asyncio
    async def test_grid_has_9_children(self, app):
        async with app.run_test() as pilot:
            from textual.containers import Grid

            grid = app.query_one("#notes-grid", Grid)
            assert len(grid.children) == 9


class TestAddNote:
    @pytest.mark.asyncio
    async def test_add_note_creates_post_it(self, app):
        async with app.run_test() as pilot:
            await pilot.press("a")
            post_its = app.query("PostIt")
            assert len(post_its) == 1

    @pytest.mark.asyncio
    async def test_add_note_removes_empty_slot(self, app):
        async with app.run_test() as pilot:
            await pilot.press("a")
            empty_slots = app.query("EmptySlot")
            assert len(empty_slots) == 8

    @pytest.mark.asyncio
    async def test_add_note_grid_stays_9(self, app):
        async with app.run_test() as pilot:
            await pilot.press("a")
            from textual.containers import Grid

            grid = app.query_one("#notes-grid", Grid)
            assert len(grid.children) == 9

    @pytest.mark.asyncio
    async def test_add_multiple_notes(self, app):
        async with app.run_test() as pilot:
            for _ in range(3):
                await pilot.press("a")
            post_its = app.query("PostIt")
            assert len(post_its) == 3

    @pytest.mark.asyncio
    async def test_add_note_unique_titles(self, app):
        async with app.run_test() as pilot:
            await pilot.press("a")
            await pilot.press("a")
            post_its = list(app.query("PostIt"))
            titles = [p.title for p in post_its]
            assert len(set(titles)) == 2  # all unique

    @pytest.mark.asyncio
    async def test_cannot_add_more_than_9(self, app):
        async with app.run_test() as pilot:
            for _ in range(10):
                await pilot.press("a")
            post_its = app.query("PostIt")
            assert len(post_its) == 9


class TestDeleteNote:
    @pytest.mark.asyncio
    async def test_delete_replaces_with_empty_slot(self, app):
        async with app.run_test() as pilot:
            await pilot.press("a")
            assert len(app.query("PostIt")) == 1
            await pilot.press("d")
            # Confirm deletion
            await pilot.press("enter")
            await pilot.pause()
            assert len(app.query("PostIt")) == 0
            assert len(app.query("EmptySlot")) == 9

    @pytest.mark.asyncio
    async def test_delete_grid_stays_9(self, app):
        async with app.run_test() as pilot:
            await pilot.press("a")
            await pilot.press("d")
            await pilot.press("enter")
            await pilot.pause()
            from textual.containers import Grid

            grid = app.query_one("#notes-grid", Grid)
            assert len(grid.children) == 9


class TestMoveMode:
    @pytest.mark.asyncio
    async def test_enter_move_mode(self, app):
        async with app.run_test() as pilot:
            await pilot.press("a")
            await pilot.press("m")
            assert app.move_mode is True

    @pytest.mark.asyncio
    async def test_exit_move_mode_escape(self, app):
        async with app.run_test() as pilot:
            await pilot.press("a")
            await pilot.press("m")
            await pilot.press("escape")
            assert app.move_mode is False

    @pytest.mark.asyncio
    async def test_move_mode_on_empty_slot_warns(self, app):
        async with app.run_test() as pilot:
            await pilot.press("m")
            assert app.move_mode is False


class TestColorIndex:
    @pytest.mark.asyncio
    async def test_post_it_has_color(self, app):
        async with app.run_test() as pilot:
            await pilot.press("a")
            post_it = app.query_one("PostIt", PostIt)
            assert 0 <= post_it.color_index <= 5
