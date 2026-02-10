"""Entry point for tui-notes application."""

from tui_notes.app import NotesApp


def main() -> None:
    """Run the tui-notes application."""
    app = NotesApp()
    app.run()


if __name__ == "__main__":
    main()
