"""
domain.py -- Pure note state. No UI, no I/O, no external dependencies.

This is the inner ring. It defines WHAT the app knows, not HOW it
stores or displays anything.

Rule: Nothing in this file may import tkinter, pathlib for I/O, or any
      UI/IO library. Data classes and pure logic only.
"""

from dataclasses import dataclass


@dataclass
class WindowSettings:
    """Presentation state for the floating window.

    Pure values. Changing them produces no side effects.
    The UI layer decides how to apply them.
    """
    always_on_top: bool = True   # default on: this is a quick-note overlay
    # Alpha as a fraction: 1.0 = fully opaque, 0.1 = nearly transparent.
    # Clamped so the window can never disappear completely.
    alpha: float = 1.0

    def with_alpha(self, alpha: float) -> "WindowSettings":
        """Return a new WindowSettings with the given alpha (clamped 0.1-1.0)."""
        clamped = max(0.1, min(1.0, alpha))
        return WindowSettings(always_on_top=self.always_on_top, alpha=clamped)

    def with_toggled_topmost(self) -> "WindowSettings":
        """Return a new WindowSettings with always_on_top flipped."""
        return WindowSettings(always_on_top=not self.always_on_top, alpha=self.alpha)


@dataclass
class NoteState:
    """Everything the note app needs to know in memory.

    - content: the text the user typed (source of truth).
    - is_dirty: True when content has changed since the last successful save.
    - window: presentation settings, a separate concern from content.
    """
    content: str = ""
    is_dirty: bool = False
    window: WindowSettings = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.window is None:
            self.window = WindowSettings()

    @property
    def display_title(self) -> str:
        """Window title reflecting unsaved state."""
        marker = " *" if self.is_dirty else ""
        return f"Quick Note{marker}"

    def with_content(self, content: str) -> "NoteState":
        """Return state after user edit, marking content as dirty."""
        return NoteState(content=content, is_dirty=True, window=self.window)

    def after_save(self) -> "NoteState":
        """Return state after a successful save: dirty flag cleared."""
        return NoteState(content=self.content, is_dirty=False, window=self.window)

    def after_load(self, content: str) -> "NoteState":
        """Return state after loading persisted content at startup."""
        return NoteState(content=content, is_dirty=False, window=self.window)

    def with_window(self, window: WindowSettings) -> "NoteState":
        """Return state with updated window settings."""
        return NoteState(content=self.content, is_dirty=self.is_dirty, window=window)
