"""Main application module for tui-notes."""

from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, TextArea, Input, Button
from textual.containers import Grid, Container, Horizontal
from textual.reactive import reactive
from textual.binding import Binding


class EditPostItScreen(ModalScreen[dict | None]):
    """Modal screen for editing a post-it note."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, title: str, content: str) -> None:
        super().__init__()
        self._edit_title = title
        self._edit_content = content

    def compose(self) -> ComposeResult:
        with Container(id="edit-modal"):
            yield Static("Edit Note", id="edit-modal-title")
            yield Input(value=self._edit_title, placeholder="Title", id="edit-title-input")
            yield TextArea(self._edit_content, id="edit-content-input")
            with Horizontal(id="edit-buttons"):
                yield Button("Save", variant="primary", id="edit-save")
                yield Button("Cancel", variant="default", id="edit-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "edit-save":
            self._do_save()
        else:
            self.dismiss(None)

    def _do_save(self) -> None:
        title = self.query_one("#edit-title-input", Input).value
        content = self.query_one("#edit-content-input", TextArea).text
        self.dismiss({"title": title, "content": content})

    def action_cancel(self) -> None:
        self.dismiss(None)


class ConfirmScreen(ModalScreen[bool]):
    """Modal screen for confirming an action."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, message: str) -> None:
        super().__init__()
        self._message = message

    def compose(self) -> ComposeResult:
        with Container(id="confirm-modal"):
            yield Static(self._message, id="confirm-message")
            with Horizontal(id="confirm-buttons"):
                yield Button("Yes", variant="error", id="confirm-yes")
                yield Button("No", variant="default", id="confirm-no")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "confirm-yes")

    def action_cancel(self) -> None:
        self.dismiss(False)


class EmptySlot(Static, can_focus=True):
    """Placeholder for an empty post-it slot."""

    def __init__(self, **kwargs) -> None:
        super().__init__("Press 'a' to add a note", **kwargs)
        self.add_class("empty-slot")

    def on_mouse_up(self, event) -> None:
        """Accept drop on mouse up."""
        self.app._finish_drag(self)
        event.stop()


class PostIt(Container, can_focus=True):
    """A single post-it note widget."""

    title: reactive[str] = reactive("")
    content: reactive[str] = reactive("")
    position: reactive[int] = reactive(0)

    def __init__(
        self, position: int, title: str = "", content: str = "", **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.position = position
        self.title = title or f"Note {position + 1}"
        self.content = content
        self.add_class(f"post-it-{position % 6}")

    def compose(self) -> ComposeResult:
        """Compose the post-it widget."""
        yield Static(self.title, classes="post-it-title")
        yield Static(self.content or "( empty )", classes="post-it-content")

    def watch_title(self, new_title: str) -> None:
        try:
            self.query_one(".post-it-title", Static).update(new_title)
        except Exception:
            pass

    def watch_content(self, new_content: str) -> None:
        try:
            self.query_one(".post-it-content", Static).update(new_content or "( empty )")
        except Exception:
            pass

    def on_mouse_down(self, event) -> None:
        """Start drag on mouse down."""
        self.app._start_drag(self)
        event.stop()

    def on_mouse_up(self, event) -> None:
        """Accept drop on mouse up."""
        self.app._finish_drag(self)
        event.stop()


class NotesApp(App):
    """A TUI application for managing post-it notes in a 3x3 grid."""

    CSS_PATH = "style.tcss"
    TITLE = "TUI Notes"
    MAX_NOTES = 9

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("a", "add_note", "Add"),
        Binding("d", "delete_note", "Delete"),
        Binding("e", "edit_note", "Edit"),
        Binding("enter", "edit_note", "Edit", show=False),
        Binding("m", "toggle_move", "Move"),
        Binding("escape", "cancel_move", "Cancel", show=False),
        Binding("question_mark", "help", "Help"),
    ]

    move_mode: reactive[bool] = reactive(False)
    _moving_post_it: PostIt | None = None
    _drag_source: PostIt | None = None

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header()
        yield Grid(
            *[EmptySlot() for _ in range(self.MAX_NOTES)],
            id="notes-grid",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Focus the first slot on mount."""
        grid = self.query_one("#notes-grid", Grid)
        first = grid.children[0]
        if first:
            first.focus()

    def _get_post_its(self) -> list[PostIt]:
        """Return all active post-its in order."""
        return list(self.query("PostIt"))

    def _rebuild_grid(self) -> None:
        """Rebuild grid with post-its followed by empty slots."""
        grid = self.query_one("#notes-grid", Grid)
        post_its = self._get_post_its()

        for i, post_it in enumerate(post_its):
            post_it.position = i

        for slot in self.query("EmptySlot"):
            slot.remove()

        empty_count = self.MAX_NOTES - len(post_its)
        for _ in range(empty_count):
            grid.mount(EmptySlot())

        self.set_timer(0.1, self._focus_first)

    def _focus_first(self) -> None:
        """Focus the first child in the grid."""
        grid = self.query_one("#notes-grid", Grid)
        if grid.children:
            grid.children[0].focus()

    def action_add_note(self) -> None:
        """Add a new post-it to the grid."""
        post_its = self._get_post_its()
        if len(post_its) >= self.MAX_NOTES:
            self.notify("Grid is full! Remove a note first.", severity="warning")
            return

        position = len(post_its)
        new_post_it = PostIt(position)

        empty_slots = list(self.query("EmptySlot"))
        if empty_slots:
            empty_slots[0].remove()

        grid = self.query_one("#notes-grid", Grid)
        remaining_slots = list(self.query("EmptySlot"))
        if remaining_slots:
            grid.mount(new_post_it, before=remaining_slots[0])
        else:
            grid.mount(new_post_it)

        new_post_it.focus()
        self.notify(f"Added: {new_post_it.title}")

    def action_delete_note(self) -> None:
        """Delete the focused post-it after confirmation."""
        focused = self.focused
        if not isinstance(focused, PostIt):
            self.notify("Select a note to delete.", severity="warning")
            return

        self.push_screen(
            ConfirmScreen(f"Delete '{focused.title}'?"),
            callback=lambda confirmed: self._do_delete(focused, confirmed),
        )

    def _do_delete(self, post_it: PostIt, confirmed: bool) -> None:
        """Remove the post-it and rearrange."""
        if not confirmed:
            return

        title = post_it.title
        post_it.remove()
        self._rebuild_grid()
        self.notify(f"Deleted: {title}")

    def action_edit_note(self) -> None:
        """Open edit modal for the focused post-it."""
        focused = self.focused
        if isinstance(focused, PostIt):
            self.push_screen(
                EditPostItScreen(focused.title, focused.content),
                callback=lambda result: self._apply_edit(focused, result),
            )

    def _apply_edit(self, post_it: PostIt, result: dict | None) -> None:
        """Apply edits from the modal to the post-it."""
        if result is not None:
            post_it.title = result["title"]
            post_it.content = result["content"]

    def action_help(self) -> None:
        """Show help information."""
        self.notify("Arrows: Navigate | a: Add | d: Delete | e/Enter: Edit | m: Move | q: Quit")

    def watch_move_mode(self, active: bool) -> None:
        """Update subtitle when move mode changes."""
        self.sub_title = "MOVE MODE - Arrows to move, Enter/Esc to exit" if active else ""

    def action_toggle_move(self) -> None:
        """Enter move mode for the focused post-it."""
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
        """Cancel move mode."""
        if self.move_mode:
            self._exit_move_mode()

    def _exit_move_mode(self) -> None:
        """Exit move mode and clean up."""
        if self._moving_post_it:
            self._moving_post_it.remove_class("moving")
            self._moving_post_it.focus()
        self._moving_post_it = None
        self.move_mode = False

    def on_key(self, event) -> None:
        """Handle arrow keys for navigation and move mode."""
        if event.key not in ("up", "down", "left", "right", "enter", "escape"):
            return

        if self.move_mode and self._moving_post_it:
            grid = self.query_one("#notes-grid", Grid)
            children = list(grid.children)
            current_idx = children.index(self._moving_post_it)
            target_idx = None
            total = len(children)

            if event.key == "up" and current_idx >= 3:
                target_idx = current_idx - 3
            elif event.key == "down" and current_idx + 3 < total:
                target_idx = current_idx + 3
            elif event.key == "left" and current_idx % 3 > 0:
                target_idx = current_idx - 1
            elif event.key == "right" and current_idx % 3 < 2 and current_idx + 1 < total:
                target_idx = current_idx + 1
            elif event.key in ("enter", "escape"):
                self._exit_move_mode()
                event.prevent_default()
                return

            if target_idx is not None:
                self._swap_positions(current_idx, target_idx)
                event.prevent_default()
            return

        # Normal mode: navigate between grid children
        if event.key in ("up", "down", "left", "right"):
            grid = self.query_one("#notes-grid", Grid)
            children = list(grid.children)
            focused = self.focused
            if focused not in children:
                return
            current_idx = children.index(focused)
            target_idx = None
            total = len(children)

            if event.key == "up" and current_idx >= 3:
                target_idx = current_idx - 3
            elif event.key == "down" and current_idx + 3 < total:
                target_idx = current_idx + 3
            elif event.key == "left" and current_idx % 3 > 0:
                target_idx = current_idx - 1
            elif event.key == "right" and current_idx % 3 < 2 and current_idx + 1 < total:
                target_idx = current_idx + 1

            if target_idx is not None:
                children[target_idx].focus()
                event.prevent_default()

    def _swap_positions(self, idx_a: int, idx_b: int) -> None:
        """Swap data between two post-its in the grid."""
        grid = self.query_one("#notes-grid", Grid)
        children = list(grid.children)

        if idx_a >= len(children) or idx_b >= len(children):
            return

        widget_a = children[idx_a]
        widget_b = children[idx_b]

        if not isinstance(widget_a, PostIt) or not isinstance(widget_b, PostIt):
            return

        widget_a.title, widget_b.title = widget_b.title, widget_a.title
        widget_a.content, widget_b.content = widget_b.content, widget_a.content

        if self._moving_post_it is widget_a:
            widget_a.remove_class("moving")
            self._moving_post_it = widget_b
            widget_b.add_class("moving")
            widget_b.focus()
        elif self._moving_post_it is widget_b:
            widget_b.remove_class("moving")
            self._moving_post_it = widget_a
            widget_a.add_class("moving")
            widget_a.focus()

    def _start_drag(self, post_it: PostIt) -> None:
        """Begin dragging a post-it."""
        if self.move_mode:
            return
        self._drag_source = post_it
        post_it.add_class("dragging")
        self.sub_title = f"Dragging '{post_it.title}' — drop on another note or slot"

    def _finish_drag(self, target) -> None:
        """Finish drag by swapping source with target."""
        if not self._drag_source:
            return

        source = self._drag_source
        source.remove_class("dragging")
        self._drag_source = None
        self.sub_title = ""

        if target is source:
            return

        grid = self.query_one("#notes-grid", Grid)
        children = list(grid.children)
        try:
            idx_a = children.index(source)
            idx_b = children.index(target)
        except ValueError:
            return

        self._swap_positions(idx_a, idx_b)
        source.focus()
