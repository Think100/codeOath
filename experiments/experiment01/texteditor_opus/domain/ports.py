"""Ports: contracts between domain and the outside world.

Outgoing ports define what the domain needs from external systems.
Incoming ports define what the outside world can ask the domain to do.
"""

from pathlib import Path
from typing import Protocol


# --- Outgoing Ports (domain needs these, adapters implement them) ---


class FileReader(Protocol):
    """Read file contents from some storage."""

    def read(self, path: Path) -> str: ...


class FileWriter(Protocol):
    """Write file contents to some storage."""

    def write(self, path: Path, content: str) -> None: ...


# --- Incoming Ports (outside world calls these, use cases implement them) ---


class OpenDocument(Protocol):
    """Open a document from a file path."""

    def execute(self, path: Path) -> None: ...


class SaveDocument(Protocol):
    """Save the current document."""

    def execute(self) -> None: ...


class SaveDocumentAs(Protocol):
    """Save the current document to a new path."""

    def execute(self, path: Path) -> None: ...


class UpdateContent(Protocol):
    """Update the document content from the editor."""

    def execute(self, new_content: str) -> None: ...
