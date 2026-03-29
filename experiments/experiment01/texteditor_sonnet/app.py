"""
app.py -- Application layer: use cases and the port contract.

This is the middle ring. It orchestrates domain state and I/O,
but knows nothing about how the UI renders things.

The EditorPort Protocol is the contract this layer exposes upward.
The UI adapter must implement it. This is "Contracts in Code":
the type checker enforces the boundary, not a comment.

Rule: This file may import domain and stdlib (pathlib, os).
      It must NOT import tkinter or any GUI library.
"""

from pathlib import Path
from typing import Protocol

from domain import EditorState, WindowSettings


# ---------------------------------------------------------------------------
# Port: the contract the application exposes to the UI layer.
# The UI implements this; the app calls back through it.
# ---------------------------------------------------------------------------

class EditorPort(Protocol):
    """Interface the UI adapter must satisfy.

    These are the only callbacks the application layer will ever invoke.
    Keeping them narrow means the application layer can be tested without
    a real UI.
    """

    def refresh_title(self, title: str) -> None:
        """Update the window title to reflect current state."""
        ...

    def refresh_content(self, content: str) -> None:
        """Replace the visible text with the given content."""
        ...

    def apply_window_settings(self, settings: WindowSettings) -> None:
        """Apply always-on-top and alpha to the native window."""
        ...

    def show_error(self, message: str) -> None:
        """Display an error to the user (dialog, status bar, etc.)."""
        ...

    def show_info(self, message: str) -> None:
        """Display a non-critical message to the user."""
        ...

    def ask_save_path(self) -> Path | None:
        """Prompt the user to choose a file path for saving. Returns None if cancelled."""
        ...

    def ask_open_path(self) -> Path | None:
        """Prompt the user to choose a file to open. Returns None if cancelled."""
        ...


# ---------------------------------------------------------------------------
# Application: use cases as methods.
# ---------------------------------------------------------------------------

class EditorApplication:
    """Orchestrates use cases for the text editor.

    Owns the single source-of-truth EditorState.
    Communicates changes back to the UI via the EditorPort.

    The ui parameter is typed as EditorPort, but we store it untyped at
    runtime to allow late binding (the UI registers itself after init).
    The type annotation serves as documentation and for static analysis.
    """

    def __init__(self) -> None:
        self._state = EditorState()
        self._ui: EditorPort | None = None

    def register_ui(self, ui: EditorPort) -> None:
        """Connect the UI adapter. Called once during startup wiring."""
        self._ui = ui
        self._push_state()

    # --- Use cases ---

    def open_file(self) -> None:
        """Use case: ask the user for a file and load it."""
        assert self._ui is not None, "UI not registered"
        path = self._ui.ask_open_path()
        if path is None:
            return
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as e:
            self._ui.show_error(f"Could not open file: {e}")
            return
        self._state = self._state.after_load(path, content)
        self._push_state()
        self._ui.refresh_content(self._state.content)

    def save_file(self) -> None:
        """Use case: save to the current file, or delegate to save_as."""
        if self._state.file_path is None:
            self.save_file_as()
        else:
            self._write_file(self._state.file_path)

    def save_file_as(self) -> None:
        """Use case: prompt for a path, then save."""
        assert self._ui is not None, "UI not registered"
        path = self._ui.ask_save_path()
        if path is None:
            return
        self._write_file(path)

    def update_content(self, content: str) -> None:
        """Use case: user edited text. Update state without refreshing the widget."""
        self._state = self._state.with_content(content)
        # Only the title needs updating (modified marker), not the text widget.
        # Pushing content back would cause a cursor-position reset on every keystroke.
        assert self._ui is not None, "UI not registered"
        self._ui.refresh_title(self._state.display_title)

    def toggle_always_on_top(self) -> None:
        """Use case: flip the always-on-top setting."""
        new_window = self._state.window.with_toggled_topmost()
        self._state = self._state.with_window(new_window)
        assert self._ui is not None, "UI not registered"
        self._ui.apply_window_settings(self._state.window)

    def set_alpha(self, alpha: float) -> None:
        """Use case: adjust window transparency. Alpha is 0.0-1.0."""
        new_window = self._state.window.with_alpha(alpha)
        self._state = self._state.with_window(new_window)
        assert self._ui is not None, "UI not registered"
        self._ui.apply_window_settings(self._state.window)

    @property
    def window_settings(self) -> WindowSettings:
        """Read-only access to current window settings (used during UI init)."""
        return self._state.window

    # --- Internal helpers ---

    def _write_file(self, path: Path) -> None:
        assert self._ui is not None, "UI not registered"
        try:
            path.write_text(self._state.content, encoding="utf-8")
        except OSError as e:
            self._ui.show_error(f"Could not save file: {e}")
            return
        self._state = self._state.after_save(path)
        self._push_state()

    def _push_state(self) -> None:
        """Synchronise UI with current state (title and window settings)."""
        assert self._ui is not None, "UI not registered"
        self._ui.refresh_title(self._state.display_title)
        self._ui.apply_window_settings(self._state.window)
