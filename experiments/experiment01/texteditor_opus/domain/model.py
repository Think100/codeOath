"""Domain model for the text editor.

Pure data structures with no external dependencies.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Document:
    """A text document with optional file origin."""

    content: str = ""
    file_path: Path | None = None
    is_modified: bool = False

    @property
    def title(self) -> str:
        if self.file_path is None:
            return "Untitled"
        return self.file_path.name

    def update_content(self, new_content: str) -> None:
        """Replace the document content and mark as modified."""
        if new_content != self.content:
            self.content = new_content
            self.is_modified = True

    def mark_saved(self, path: Path) -> None:
        """Mark the document as saved to the given path."""
        self.file_path = path
        self.is_modified = False


@dataclass
class WindowState:
    """UI-agnostic representation of window preferences."""

    always_on_top: bool = False
    opacity: float = 1.0  # 0.0 = fully transparent, 1.0 = fully opaque

    OPACITY_MIN: float = field(default=0.1, init=False, repr=False)
    OPACITY_MAX: float = field(default=1.0, init=False, repr=False)

    def set_opacity(self, value: float) -> None:
        """Clamp opacity to valid range."""
        self.opacity = max(self.OPACITY_MIN, min(self.OPACITY_MAX, value))

    def toggle_always_on_top(self) -> None:
        self.always_on_top = not self.always_on_top
