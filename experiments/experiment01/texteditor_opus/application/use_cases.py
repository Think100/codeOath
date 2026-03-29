"""Use cases: orchestrate domain logic with outgoing ports.

This layer knows about the domain and ports, but never about concrete adapters.
Each use case implements an incoming port.
"""

from pathlib import Path

from domain.model import Document
from domain.ports import FileReader, FileWriter


class OpenDocumentUseCase:
    """Load a file into the document model."""

    def __init__(self, document: Document, reader: FileReader) -> None:
        self._document = document
        self._reader = reader

    def execute(self, path: Path) -> None:
        content = self._reader.read(path)
        self._document.content = content
        self._document.file_path = path
        self._document.is_modified = False


class SaveDocumentUseCase:
    """Save the current document to its existing path."""

    def __init__(self, document: Document, writer: FileWriter) -> None:
        self._document = document
        self._writer = writer

    def execute(self) -> None:
        if self._document.file_path is None:
            raise ValueError("No file path set. Use SaveAs instead.")
        self._writer.write(self._document.file_path, self._document.content)
        self._document.mark_saved(self._document.file_path)


class SaveDocumentAsUseCase:
    """Save the current document to a new path."""

    def __init__(self, document: Document, writer: FileWriter) -> None:
        self._document = document
        self._writer = writer

    def execute(self, path: Path) -> None:
        self._writer.write(path, self._document.content)
        self._document.mark_saved(path)


class UpdateContentUseCase:
    """Sync editor content into the domain model."""

    def __init__(self, document: Document) -> None:
        self._document = document

    def execute(self, new_content: str) -> None:
        self._document.update_content(new_content)
