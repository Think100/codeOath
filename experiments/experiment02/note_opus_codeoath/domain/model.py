"""Domain model for the note-taking app.

Pure data structures with no external dependencies.
"""

from dataclasses import dataclass, field


@dataclass
class Note:
    """A single text note with auto-save tracking."""

    content: str = ""
    is_dirty: bool = False

    def update_content(self, new_content: str) -> None:
        """Replace the note content and mark as needing save."""
        if new_content != self.content:
            self.content = new_content
            self.is_dirty = True

    def mark_saved(self) -> None:
        """Mark the note as persisted."""
        self.is_dirty = False


@dataclass
class WindowState:
    """UI-agnostic representation of window preferences."""

    always_on_top: bool = False
    opacity: float = 1.0

    OPACITY_MIN: float = field(default=0.1, init=False, repr=False)
    OPACITY_MAX: float = field(default=1.0, init=False, repr=False)

    def set_opacity(self, value: float) -> None:
        """Clamp opacity to valid range."""
        self.opacity = max(self.OPACITY_MIN, min(self.OPACITY_MAX, value))

    def toggle_always_on_top(self) -> None:
        self.always_on_top = not self.always_on_top
