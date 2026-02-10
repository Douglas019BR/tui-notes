# TUI Notes

A terminal-based notes application for quick note-taking and organization, right from your command line.

## Overview

TUI Notes is a lightweight, keyboard-driven notes manager that works entirely in your terminal. Think of it as multiple post-it notes in your CLI - create, edit, organize, and manage notes without ever leaving your terminal environment.

## Features (Planned)

- **Multiple Notes**: Create and manage multiple notes simultaneously
- **Persistent Storage**: All notes are saved automatically and persist between sessions
- **Easy Organization**: Reorder notes to prioritize what matters
- **Clean Interface**: Intuitive terminal UI built with modern TUI libraries
- **Quick Access**: Launch from anywhere in your terminal
- **Note Management**: 
  - Add new notes with custom titles
  - Edit note content
  - Delete notes when no longer needed
  - Clear note content while keeping the note
  - Reorganize note order

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd tui-notes

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m tui_notes
```

## Usage

```bash
# Launch the application
tui-notes

# Your notes will be automatically saved in ~/.tui-notes/
```

### Keyboard Shortcuts (Planned)

- `Ctrl+N` - Create new note
- `Tab` - Switch between notes
- `Ctrl+D` - Delete current note
- `Ctrl+C` - Clear note content
- `Ctrl+Q` - Quit application
- Arrow keys - Navigate and reorder notes

## Data Storage

Notes are stored locally in `~/.tui-notes/notes.json` and persist across sessions.

## Requirements

- Python 3.8+
- Terminal with color support

## Development Status

🚧 **In Development** - This project is currently in the planning and initial implementation phase.

## License

See LICENSE file for details.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
