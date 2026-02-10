# TUI Notes - Implementation Context

This document contains technical details, architectural decisions, and implementation guidance for continuing development of the TUI Notes project.

## Project Vision

A terminal-based notes application inspired by post-it notes, allowing users to quickly capture and organize thoughts directly from the command line with persistent storage.

## Technology Stack

### Core Technologies

- **Language**: Python 3.8+
- **TUI Framework**: Textual (recommended) or Rich
  - **Why Textual**: Modern, reactive, async-based, great documentation, web-dev-friendly component model
  - Alternative: Rich (simpler but less powerful for complex layouts)
- **Data Persistence**: JSON file storage
- **Data Location**: `~/.tui-notes/notes.json` (user home directory)

### Dependencies (Planned)

```
textual>=0.40.0
pydantic>=2.0.0  # For data validation (optional)
```

## Architecture Overview

### Project Structure

```
tui-notes/
├── tui_notes/
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── app.py               # Main Textual app
│   ├── models.py            # Note data models
│   ├── storage.py           # File persistence layer
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── note_card.py     # Individual note widget
│   │   └── note_list.py     # Container for multiple notes
│   └── config.py            # Configuration and paths
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_storage.py
├── README.md
├── CONTEXT.md
├── requirements.txt
├── setup.py
└── LICENSE
```

### Data Model

```python
# models.py
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Note:
    id: str                    # UUID
    title: str                 # Note title
    content: str               # Note content
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last modified timestamp
    order: int                 # Display order

@dataclass
class NotesData:
    notes: List[Note]
    version: str = "1.0"       # For future migration support
```

### Storage Layer

**File Location**: `~/.tui-notes/notes.json`

**Operations**:
- `load_notes()` -> NotesData
- `save_notes(notes: NotesData)` -> None
- `create_note(title: str, content: str)` -> Note
- `update_note(note_id: str, updates: dict)` -> Note
- `delete_note(note_id: str)` -> None
- `reorder_notes(note_ids: List[str])` -> None

**Implementation Details**:
- Use `pathlib.Path.home()` for cross-platform home directory
- Create directory if it doesn't exist
- Handle JSON encoding/decoding with datetime support
- Atomic writes (write to temp file, then rename)
- Backup mechanism before overwriting

### UI Components

#### Main App Layout (Textual)

```
┌─────────────────────────────────────┐
│  TUI Notes - Press Ctrl+Q to quit  │ ← Header
├─────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐│
│ │ Note 1  │ │ Note 2  │ │ Note 3  ││
│ │ Title   │ │ Title   │ │ Title   ││ ← Note Cards (scrollable grid)
│ │         │ │         │ │         ││
│ │ Content │ │ Content │ │ Content ││
│ │ ...     │ │ ...     │ │ ...     ││
│ └─────────┘ └─────────┘ └─────────┘│
├─────────────────────────────────────┤
│ Ctrl+N: New | Tab: Navigate | ...  │ ← Footer (shortcuts)
└─────────────────────────────────────┘
```

#### Widget Hierarchy

- **NotesApp** (Textual App)
  - **Header** (built-in)
  - **NoteList** (Container widget)
    - **NoteCard** (Custom widget per note)
      - Title input
      - Content textarea
      - Metadata (created/updated)
  - **Footer** (built-in)

### Key Features Implementation

#### 1. Note Creation
- Keyboard shortcut triggers modal/dialog
- User inputs title
- New note added with empty content
- Focus moves to new note
- Auto-save triggered

#### 2. Note Editing
- Focus on note card makes it editable
- Textual's `Input` and `TextArea` widgets
- Reactive updates trigger auto-save (with debouncing)

#### 3. Note Deletion
- Keyboard shortcut or button
- Confirmation dialog (optional)
- Remove from storage
- Update UI

#### 4. Note Reordering
- Drag-and-drop (if Textual supports) OR
- Arrow keys + modifier to move position
- Update order property
- Re-render list

#### 5. Persistence
- Auto-save on every change (debounced 1-2 seconds)
- Manual save on quit
- Load on startup

### Configuration

```python
# config.py
from pathlib import Path

# Paths
APP_DIR = Path.home() / ".tui-notes"
NOTES_FILE = APP_DIR / "notes.json"
BACKUP_DIR = APP_DIR / "backups"

# Settings
AUTO_SAVE_DELAY = 2  # seconds
MAX_BACKUPS = 5
DEFAULT_NOTE_TITLE = "Untitled Note"
```

## Implementation Phases

### Phase 1: Foundation
- [ ] Set up project structure
- [ ] Implement data models
- [ ] Create storage layer with JSON persistence
- [ ] Write basic tests for storage

### Phase 2: Basic UI
- [ ] Create main Textual app skeleton
- [ ] Implement single note card widget
- [ ] Add note list container
- [ ] Test loading/saving notes

### Phase 3: Core Features
- [ ] Add note creation
- [ ] Implement note editing
- [ ] Add note deletion
- [ ] Implement keyboard shortcuts

### Phase 4: Advanced Features
- [ ] Note reordering
- [ ] Clear note content
- [ ] Search/filter notes
- [ ] Note categories/tags (future)

### Phase 5: Polish
- [ ] Error handling
- [ ] User feedback (toasts/notifications)
- [ ] Themes/colors
- [ ] Performance optimization
- [ ] Comprehensive testing

## Technical Considerations

### Async/Await
Textual is async-based. Key points:
- App methods are async
- Event handlers are async
- Use `await` for I/O operations

### State Management
- App-level state for notes list
- Reactive properties for UI updates
- Textual's reactive system handles re-rendering

### Error Handling
- File permission errors
- Corrupted JSON data
- Disk full scenarios
- Invalid user input

### Testing Strategy
- Unit tests for models and storage
- Integration tests for storage + models
- Snapshot tests for UI components (Textual supports this)
- Manual testing for keyboard interactions

## Development Commands

```bash
# Development setup
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Run app
python -m tui_notes

# Run tests
pytest

# Format code
black tui_notes/
isort tui_notes/

# Type checking
mypy tui_notes/
```

## Resources

- **Textual Documentation**: https://textual.textualize.io/
- **Textual Tutorial**: https://textual.textualize.io/tutorial/
- **Textual Examples**: https://github.com/Textualize/textual/tree/main/examples
- **Rich Documentation**: https://rich.readthedocs.io/

## Next Steps for Implementation

1. Start with Textual tutorial to understand the framework
2. Create basic project structure
3. Implement data models with tests
4. Build storage layer with file I/O
5. Create simplest possible UI (one note card)
6. Iterate and add features incrementally

## Design Decisions Log

- **Why JSON over SQLite?**: Simpler for small dataset, human-readable, easy backup
- **Why Textual over Curses?**: Modern, better DX, reactive model, active development
- **Why local files over cloud?**: Privacy, offline-first, simplicity, no dependencies
- **Data location**: User home directory follows Unix convention for user data

## Future Enhancements

- Export notes to markdown
- Import from other formats
- Sync between devices (optional)
- Note templates
- Rich text formatting (limited by terminal)
- Tags and categories
- Search functionality
- Dark/light themes
- Note sharing/export
