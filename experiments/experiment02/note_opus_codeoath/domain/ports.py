"""Ports: contracts between domain and the outside world.

Outgoing ports define what the domain needs from external systems.
Incoming ports define what the outside world can ask the domain to do.
"""

from typing import Protocol


# --- Outgoing Ports (domain needs these, adapters implement them) ---


class NoteStorage(Protocol):
    """Persist and retrieve note content."""

    def load(self) -> str: ...

    def save(self, content: str) -> None: ...


# --- Incoming Ports (outside world calls these, use cases implement them) ---


class LoadNote(Protocol):
    """Load the persisted note into the domain model."""

    def execute(self) -> None: ...


class SaveNote(Protocol):
    """Persist the current note content."""

    def execute(self) -> None: ...


class UpdateNote(Protocol):
    """Update the note content from the editor."""

    def execute(self, new_content: str) -> None: ...
