"""
domain.py -- Pure editor state. No UI, no I/O, no external dependencies.

This is the inner ring of the ports-and-adapters architecture.
It defines WHAT the editor knows, not HOW it presents itself.

Rule: Nothing in this file may import tkinter or any UI/IO library.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class WindowSettings:
    """Immutable-style settings for window presentation.

    These are pure values. Changing them does not trigger side effects.
    The UI layer decides what to do with them.
    """
    always_on_top: bool = False
    # Alpha as a fraction: 1.0 = fully opaque, 0.1 = nearly transparent.
    # Minimum is clamped at 0.1 to prevent the window from disappearing.
    alpha: float = 1.0

    def with_alpha(self, alpha: float) -> "WindowSettings":
        """Return a new WindowSettings with the given alpha value (clamped)."""
        clamped = max(0.1, min(1.0, alpha))
        return WindowSettings(always_on_top=self.always_on_top, alpha=clamped)

    def with_toggled_topmost(self) -> "WindowSettings":
        """Return a new WindowSettings with always_on_top flipped."""
        return WindowSettings(always_on_top=not self.always_on_top, alpha=self.alpha)


@dataclass
class EditorState:
    """Represents everything the editor needs to know about the current session.

    - file_path: the open file, or None if unsaved.
    - content: the current text content (source of truth in-memory).
    - is_modified: True if content differs from what was last saved/loaded.
    - window: presentation settings, separate concern from file state.
    """
    file_path: Path | None = None
    content: str = ""
    is_modified: bool = False
    window: WindowSettings = field(default_factory=WindowSettings)

    @property
    def display_title(self) -> str:
        """Human-readable window title reflecting current state."""
        name = self.file_path.name if self.file_path else "Unsaved"
        marker = " *" if self.is_modified else ""
        return f"Text Editor -- {name}{marker}"

    def with_content(self, content: str) -> "EditorState":
        """Return state after user edits, marking the document as modified."""
        return EditorState(
            file_path=self.file_path,
            content=content,
            is_modified=True,
            window=self.window,
        )

    def after_save(self, file_path: Path) -> "EditorState":
        """Return state after a successful save: cleared modified flag, updated path."""
        return EditorState(
            file_path=file_path,
            content=self.content,
            is_modified=False,
            window=self.window,
        )

    def after_load(self, file_path: Path, content: str) -> "EditorState":
        """Return state after loading a file from disk."""
        return EditorState(
            file_path=file_path,
            content=content,
            is_modified=False,
            window=self.window,
        )

    def with_window(self, window: WindowSettings) -> "EditorState":
        """Return state with updated window settings."""
        return EditorState(
            file_path=self.file_path,
            content=self.content,
            is_modified=self.is_modified,
            window=window,
        )
