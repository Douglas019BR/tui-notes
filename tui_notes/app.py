"""Main application module for tui-notes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.events import Key
from textual.reactive import reactive
from textual.widgets import Footer, Header

from tui_notes.constants import GRID_COLUMNS, MAX_NOTES
from tui_notes.screens import ColorPickerScreen, ConfirmScreen, EditPostItScreen, HelpScreen
from tui_notes.storage import load_notes, save_notes
from tui_notes.widgets import EmptySlot, PostIt


class NotesApp(App):
    """A TUI application for managing post-it notes in a 3x3 grid."""

    CSS_PATH = "style.tcss"
    TITLE = "TUI Notes"

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("a", "add_note", "Add"),
        Binding("d", "delete_note", "Delete"),
        Binding("e", "edit_note", "Edit"),
        Binding("enter", "edit_note", "Edit", show=False),
        Binding("c", "change_color", "Color"),
        Binding("m", "toggle_move", "Move"),
        Binding("escape", "cancel_move", "Cancel", show=False),
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+r", "reload", "Reload"),
        Binding("ctrl+e", "export", "Export"),
        Binding("question_mark", "help", "Help"),
    ]

    move_mode: reactive[bool] = reactive(False)
    _moving_post_it: PostIt | None = None
    _note_counter: int = 0

    # ── Lifecycle ───────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        """Compose the application layout with header, grid, and footer."""
        yield Header()
        yield Grid(
            *[EmptySlot() for _ in range(MAX_NOTES)],
            id="notes-grid",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Load saved notes from disk and focus the first slot."""
        self._load_from_disk()
        self._focus_first()

    # ── Grid helpers ────────────────────────────────────────────

    def _get_grid(self) -> Grid:
        """Return the notes grid widget.

        Returns:
            The Grid container holding all post-its and empty slots.
        """
        return self.query_one("#notes-grid", Grid)

    def _get_post_its(self) -> list[PostIt]:
        """Return all active post-it widgets in DOM order.

        Returns:
            List of PostIt widgets currently in the grid.
        """
        return list(self.query(PostIt))

    def _focus_first(self) -> None:
        """Focus the first child in the grid."""
        grid = self._get_grid()
        if grid.children:
            grid.children[0].focus()

    # ── Persistence ─────────────────────────────────────────────

    def _save_to_disk(self) -> None:
        """Serialize all post-its and save to the JSON file."""
        grid = self._get_grid()
        children = list(grid.children)
        data: list[dict[str, Any]] = [
            child.to_dict(grid_index=idx)
            for idx, child in enumerate(children)
            if isinstance(child, PostIt)
        ]
        try:
            save_notes(data)
        except OSError as exc:
            self.notify(f"Save error: {exc}", severity="error")

    def _load_from_disk(self) -> None:
        """Load post-its from disk and place them at their saved positions."""
        notes = load_notes()
        if not notes:
            return

        grid = self._get_grid()
        children = list(grid.children)

        for note in notes:
            pos = note["position"]
            if (
                0 <= pos < MAX_NOTES
                and pos < len(children)
                and isinstance(children[pos], EmptySlot)
            ):
                post_it = PostIt.from_dict(note)
                grid.mount(post_it, before=children[pos])
                children[pos].remove()
                self._note_counter += 1

    def action_save(self) -> None:
        """Save notes to disk manually."""
        self._save_to_disk()
        self.notify("Notes saved!")

    def action_reload(self) -> None:
        """Reload all notes from disk, discarding unsaved changes."""
        grid = self._get_grid()
        for child in list(grid.children):
            child.remove()
        for _ in range(MAX_NOTES):
            grid.mount(EmptySlot())
        self._note_counter = 0
        self._load_from_disk()
        self.set_timer(0.1, self._focus_first)
        self.notify("Notes reloaded!")

    # ── CRUD actions ────────────────────────────────────────────

    def action_add_note(self) -> None:
        """Add a new post-it at the focused position (or next available)."""
        post_its = self._get_post_its()
        if len(post_its) >= MAX_NOTES:
            self.notify("Grid is full! Remove a note first.", severity="warning")
            return

        focused = self.focused
        grid = self._get_grid()
        children = list(grid.children)

        idx = children.index(focused) if isinstance(focused, EmptySlot) else len(post_its)

        self._note_counter += 1
        new_post_it = PostIt(idx, title=f"Note {self._note_counter}")

        if isinstance(focused, EmptySlot):
            grid.mount(new_post_it, before=focused)
            focused.remove()
        else:
            empty_slots = list(self.query("EmptySlot"))
            if empty_slots:
                empty_slots[-1].remove()
            grid.mount(new_post_it)

        new_post_it.focus()
        self.notify(f"Added: {new_post_it.title}")
        self._save_to_disk()

    def action_delete_note(self) -> None:
        """Delete the focused post-it after user confirmation."""
        focused = self.focused
        if not isinstance(focused, PostIt):
            self.notify("Select a note to delete.", severity="warning")
            return

        self.push_screen(
            ConfirmScreen(f"Delete '{focused.title}'?"),
            callback=lambda confirmed: self._do_delete(focused, confirmed),
        )

    def _do_delete(self, post_it: PostIt, confirmed: bool) -> None:
        """Replace the confirmed post-it with an empty slot in-place.

        Args:
            post_it: The PostIt widget to remove.
            confirmed: Whether the user confirmed the deletion.
        """
        if not confirmed:
            return

        title = post_it.title
        self._note_counter -= 1
        grid = self._get_grid()
        empty = EmptySlot()
        grid.mount(empty, before=post_it)
        post_it.remove()
        empty.focus()
        self.notify(f"Deleted: {title}")
        self._save_to_disk()

    def action_edit_note(self) -> None:
        """Open the edit modal for the focused post-it."""
        focused = self.focused
        if isinstance(focused, PostIt):
            self.push_screen(
                EditPostItScreen(focused.title, focused.content),
                callback=lambda result: self._apply_edit(focused, result),
            )

    def _apply_edit(self, post_it: PostIt, result: dict[str, str] | None) -> None:
        """Apply edits returned from the edit modal.

        Args:
            post_it: The PostIt widget being edited.
            result: Dict with 'title' and 'content' keys, or None if cancelled.
        """
        if result is not None:
            post_it.title = result["title"]
            post_it.content = result["content"]
            self._save_to_disk()

    # ── Color ───────────────────────────────────────────────────

    def action_change_color(self) -> None:
        """Open the color picker for the focused post-it."""
        focused = self.focused
        if not isinstance(focused, PostIt):
            self.notify("Select a note to change color.", severity="warning")
            return
        self.push_screen(
            ColorPickerScreen(),
            callback=lambda idx: self._apply_color(focused, idx),
        )

    def _apply_color(self, post_it: PostIt, color_idx: int | None) -> None:
        """Apply the selected color to a post-it.

        Args:
            post_it: The PostIt widget to recolor.
            color_idx: Selected palette index, or None if cancelled.
        """
        if color_idx is not None:
            post_it.color_index = color_idx
            self._save_to_disk()

    # ── Export ──────────────────────────────────────────────────

    def action_export(self) -> None:
        """Export all post-its to a Markdown file in the user's home directory."""
        post_its = self._get_post_its()
        if not post_its:
            self.notify("No notes to export.", severity="warning")
            return

        lines = ["# TUI Notes Export\n"]
        for post_it in post_its:
            lines.append(f"## {post_it.title}\n")
            if post_it.content:
                lines.append(f"{post_it.content}\n")
            lines.append("")

        export_path = Path.home() / "tui-notes-export.md"
        try:
            export_path.write_text("\n".join(lines), encoding="utf-8")
            self.notify(f"Exported to {export_path}")
        except OSError as exc:
            self.notify(f"Export error: {exc}", severity="error")

    # ── Help ────────────────────────────────────────────────────

    def action_help(self) -> None:
        """Show the help screen with all keyboard shortcuts."""
        self.push_screen(HelpScreen())

    # ── Move mode ───────────────────────────────────────────────

    def watch_move_mode(self, active: bool) -> None:
        """Update the subtitle bar when move mode toggles.

        Args:
            active: Whether move mode is now active.
        """
        self.sub_title = "MOVE MODE - Arrows to move, Enter/Esc to exit" if active else ""

    def action_toggle_move(self) -> None:
        """Enter or exit move mode for the focused post-it."""
        focused = self.focused
        if not isinstance(focused, PostIt):
            self.notify("Select a note to move.", severity="warning")
            return

        if self.move_mode:
            self._exit_move_mode()
        else:
            self._moving_post_it = focused
            focused.add_class("moving")
            self.move_mode = True

    def action_cancel_move(self) -> None:
        """Cancel move mode via Escape."""
        if self.move_mode:
            self._exit_move_mode()

    def _exit_move_mode(self) -> None:
        """Exit move mode and remove visual indicators."""
        if self._moving_post_it:
            self._moving_post_it.remove_class("moving")
            self._moving_post_it.focus()
        self._moving_post_it = None
        self.move_mode = False

    # ── Navigation ──────────────────────────────────────────────

    @staticmethod
    def _calc_target_idx(key: str, current_idx: int, total: int) -> int | None:
        """Calculate the target grid index for an arrow-key press.

        Args:
            key: The key name ('up', 'down', 'left', 'right').
            current_idx: Current position in the flat grid.
            total: Total number of grid children.

        Returns:
            Target index, or None if the move is out of bounds.
        """
        if key == "up" and current_idx >= GRID_COLUMNS:
            return current_idx - GRID_COLUMNS
        if key == "down" and current_idx + GRID_COLUMNS < total:
            return current_idx + GRID_COLUMNS
        if key == "left" and current_idx % GRID_COLUMNS > 0:
            return current_idx - 1
        if (
            key == "right"
            and current_idx % GRID_COLUMNS < GRID_COLUMNS - 1
            and current_idx + 1 < total
        ):
            return current_idx + 1
        return None

    def on_key(self, event: Key) -> None:
        """Handle arrow keys for grid navigation and move mode.

        Args:
            event: The key event from Textual.
        """
        if event.key not in ("up", "down", "left", "right", "enter", "escape"):
            return

        if self.move_mode and self._moving_post_it:
            if event.key in ("enter", "escape"):
                self._exit_move_mode()
                event.prevent_default()
                return

            grid = self._get_grid()
            children = list(grid.children)
            current_idx = children.index(self._moving_post_it)
            target_idx = self._calc_target_idx(event.key, current_idx, len(children))

            if target_idx is not None:
                self._swap_positions(current_idx, target_idx)
                event.prevent_default()
            return

        if event.key in ("up", "down", "left", "right"):
            grid = self._get_grid()
            children = list(grid.children)
            focused = self.focused
            if focused not in children:
                return
            current_idx = children.index(focused)
            target_idx = self._calc_target_idx(event.key, current_idx, len(children))

            if target_idx is not None:
                children[target_idx].focus()
                event.prevent_default()

    # ── Swap logic ──────────────────────────────────────────────

    def _swap_positions(self, idx_a: int, idx_b: int) -> None:
        """Swap two grid positions. Supports PostIt↔PostIt and PostIt↔EmptySlot.

        Args:
            idx_a: First grid index.
            idx_b: Second grid index.
        """
        grid = self._get_grid()
        children = list(grid.children)

        if idx_a >= len(children) or idx_b >= len(children):
            return

        widget_a = children[idx_a]
        widget_b = children[idx_b]

        if isinstance(widget_a, PostIt) and isinstance(widget_b, PostIt):
            self._swap_post_its(widget_a, widget_b)
        elif isinstance(widget_a, PostIt) and isinstance(widget_b, EmptySlot):
            self._move_to_empty(widget_a, widget_b, idx_b, grid)
        elif isinstance(widget_a, EmptySlot) and isinstance(widget_b, PostIt):
            self._move_to_empty(widget_b, widget_a, idx_a, grid)

        self._save_to_disk()

    def _swap_post_its(self, widget_a: PostIt, widget_b: PostIt) -> None:
        """Swap data between two PostIt widgets and update move-mode tracking.

        Args:
            widget_a: First post-it.
            widget_b: Second post-it.
        """
        widget_a.title, widget_b.title = widget_b.title, widget_a.title
        widget_a.content, widget_b.content = widget_b.content, widget_a.content
        widget_a.color_index, widget_b.color_index = widget_b.color_index, widget_a.color_index

        if self._moving_post_it is widget_a:
            self._transfer_moving_class(widget_a, widget_b)
        elif self._moving_post_it is widget_b:
            self._transfer_moving_class(widget_b, widget_a)

    def _move_to_empty(
        self, post_it: PostIt, empty: EmptySlot, target_idx: int, grid: Grid
    ) -> None:
        """Move a PostIt to an EmptySlot position, leaving an EmptySlot behind.

        Args:
            post_it: The post-it being moved.
            empty: The empty slot at the target position.
            target_idx: The grid index of the target position.
            grid: The grid container.
        """
        new_post = PostIt.from_dict(post_it.to_dict(grid_index=target_idx))
        new_empty = EmptySlot()

        grid.mount(new_post, before=empty)
        empty.remove()
        grid.mount(new_empty, before=post_it)
        post_it.remove()

        if self._moving_post_it is post_it:
            self._moving_post_it = new_post
        new_post.add_class("moving")
        new_post.focus()

    def _transfer_moving_class(self, from_widget: PostIt, to_widget: PostIt) -> None:
        """Transfer the 'moving' visual class from one post-it to another.

        Args:
            from_widget: The post-it losing the moving state.
            to_widget: The post-it gaining the moving state.
        """
        from_widget.remove_class("moving")
        self._moving_post_it = to_widget
        to_widget.add_class("moving")
        to_widget.focus()
