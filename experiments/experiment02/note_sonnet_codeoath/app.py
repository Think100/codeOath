"""
app.py -- Application layer: use cases and the port contract.

Middle ring. Orchestrates domain state, persistence I/O, and the
autosave timer signal. Knows nothing about how the UI renders things.

The NotePort Protocol is the contract this layer exposes upward.
The UI adapter must implement it. This is "Contracts in Code":
the type checker enforces the boundary, not a comment.

Dependency direction: app.py -> domain.py
Rule: This file may import domain and stdlib only.
      It must NOT import tkinter or any GUI library.
"""

from pathlib import Path
from typing import Protocol

from domain import NoteState, WindowSettings


# ---------------------------------------------------------------------------
# Persistence path: stored next to this file so the app is self-contained.
# ---------------------------------------------------------------------------

_NOTE_FILE: Path = Path(__file__).parent / "note.txt"


# ---------------------------------------------------------------------------
# Port: the contract the application exposes to the UI layer.
# ---------------------------------------------------------------------------

class NotePort(Protocol):
    """Interface the UI adapter must satisfy.

    These are the only callbacks the application layer will ever invoke.
    A narrow interface means the application layer can be tested without
    a real window.
    """

    def refresh_title(self, title: str) -> None:
        """Update the window title to reflect current state."""
        ...

    def refresh_content(self, content: str) -> None:
        """Replace the visible text with the given content (used on load)."""
        ...

    def apply_window_settings(self, settings: WindowSettings) -> None:
        """Apply always-on-top and alpha to the native window."""
        ...

    def show_error(self, message: str) -> None:
        """Display an error to the user without blocking (status bar or dialog)."""
        ...

    def show_status(self, message: str) -> None:
        """Show a transient status message (e.g. 'Saved')."""
        ...


# ---------------------------------------------------------------------------
# Application: use cases as methods.
# ---------------------------------------------------------------------------

class NoteApplication:
    """Orchestrates the single-note use cases.

    Owns the single source-of-truth NoteState.
    Communicates changes back to the UI via the NotePort.

    Autosave is driven by the UI layer's timer, which calls
    autosave_tick() on a regular interval. This keeps the timer
    mechanism in the UI (where it belongs) while the save decision
    lives here (where it belongs).
    """

    def __init__(self) -> None:
        self._state = NoteState()
        self._ui: NotePort | None = None

    def register_ui(self, ui: NotePort) -> None:
        """Connect the UI adapter. Called once during startup wiring.

        Triggers the initial load so the UI shows persisted content
        as soon as the window is ready.
        """
        self._ui = ui
        self._load_persisted()
        self._push_state()

    # --- Use cases ---

    def update_content(self, content: str) -> None:
        """Use case: user edited text. Mark dirty; do not refresh the widget.

        Pushing content back into the text widget would reset the cursor
        on every keystroke. Only the title needs updating (dirty marker).
        """
        self._state = self._state.with_content(content)
        assert self._ui is not None
        self._ui.refresh_title(self._state.display_title)

    def autosave_tick(self) -> None:
        """Use case: called by the UI timer every N milliseconds.

        Saves only when content has changed since the last save.
        No-ops otherwise, so disk I/O is minimal.
        """
        if self._state.is_dirty:
            self._save()

    def save_now(self) -> None:
        """Use case: force an immediate save (e.g. on window close)."""
        self._save()

    def toggle_always_on_top(self) -> None:
        """Use case: flip the always-on-top setting."""
        new_window = self._state.window.with_toggled_topmost()
        self._state = self._state.with_window(new_window)
        assert self._ui is not None
        self._ui.apply_window_settings(self._state.window)

    def set_alpha(self, alpha: float) -> None:
        """Use case: adjust window transparency. Alpha is 0.0-1.0."""
        new_window = self._state.window.with_alpha(alpha)
        self._state = self._state.with_window(new_window)
        assert self._ui is not None
        self._ui.apply_window_settings(self._state.window)

    @property
    def window_settings(self) -> WindowSettings:
        """Read-only access to current window settings (used during UI init)."""
        return self._state.window

    # --- Internal helpers ---

    def _save(self) -> None:
        assert self._ui is not None
        try:
            _NOTE_FILE.write_text(self._state.content, encoding="utf-8")
        except OSError as exc:
            self._ui.show_error(f"Save failed: {exc}")
            return
        self._state = self._state.after_save()
        self._ui.refresh_title(self._state.display_title)
        self._ui.show_status("Saved")

    def _load_persisted(self) -> None:
        """Load the note from disk if the file exists. Silently skip if absent."""
        assert self._ui is not None
        if not _NOTE_FILE.exists():
            return
        try:
            content = _NOTE_FILE.read_text(encoding="utf-8")
        except OSError as exc:
            self._ui.show_error(f"Could not load saved note: {exc}")
            return
        self._state = self._state.after_load(content)
        self._ui.refresh_content(self._state.content)

    def _push_state(self) -> None:
        """Synchronise UI with current state (title and window settings)."""
        assert self._ui is not None
        self._ui.refresh_title(self._state.display_title)
        self._ui.apply_window_settings(self._state.window)
