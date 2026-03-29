"""Application-wide constants and default settings."""

from pathlib import Path

APP_TITLE = "Quick Note"
DEFAULT_WINDOW_SIZE = "420x340"

# Where the note is persisted between sessions.
# Stored next to this file so the app is self-contained.
NOTE_FILE: Path = Path(__file__).parent / "note.txt"

# Autosave: milliseconds between idle-triggered saves.
AUTOSAVE_DELAY_MS = 1_000

# Transparency range (0.0 = invisible, 1.0 = fully opaque)
MIN_OPACITY = 0.1
MAX_OPACITY = 1.0
DEFAULT_OPACITY = 1.0

# Font used in the text area
FONT = ("Segoe UI", 11)
