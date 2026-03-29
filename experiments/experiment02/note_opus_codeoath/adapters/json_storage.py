"""Outgoing adapter: JSON file implementation of NoteStorage.

Implements the outgoing port defined in domain/ports.py.
Stores note content in a JSON file next to the application.
"""

import json
from pathlib import Path


class JsonNoteStorage:
    """Read and write note content to a local JSON file."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def load(self) -> str:
        if not self._file_path.exists():
            return ""
        data = json.loads(self._file_path.read_text(encoding="utf-8"))
        return data.get("content", "")

    def save(self, content: str) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps({"content": content}, ensure_ascii=False, indent=2)
        self._file_path.write_text(payload, encoding="utf-8")
