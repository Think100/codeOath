"""Use cases: orchestrate domain logic with outgoing ports.

This layer knows about the domain and ports, but never about concrete adapters.
Each use case implements an incoming port.
"""

from domain.model import Note
from domain.ports import NoteStorage


class LoadNoteUseCase:
    """Load persisted content into the note model."""

    def __init__(self, note: Note, storage: NoteStorage) -> None:
        self._note = note
        self._storage = storage

    def execute(self) -> None:
        content = self._storage.load()
        self._note.content = content
        self._note.is_dirty = False


class SaveNoteUseCase:
    """Persist the current note content if it has changed."""

    def __init__(self, note: Note, storage: NoteStorage) -> None:
        self._note = note
        self._storage = storage

    def execute(self) -> None:
        if not self._note.is_dirty:
            return
        self._storage.save(self._note.content)
        self._note.mark_saved()


class UpdateNoteUseCase:
    """Sync editor content into the domain model."""

    def __init__(self, note: Note) -> None:
        self._note = note

    def execute(self, new_content: str) -> None:
        self._note.update_content(new_content)
