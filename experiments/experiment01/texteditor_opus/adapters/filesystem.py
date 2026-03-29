"""Outgoing adapter: filesystem implementation of FileReader and FileWriter.

Implements the outgoing ports defined in domain/ports.py.
"""

from pathlib import Path


class LocalFileReader:
    """Read files from the local filesystem."""

    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")


class LocalFileWriter:
    """Write files to the local filesystem."""

    def write(self, path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")
