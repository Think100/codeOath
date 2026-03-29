"""Composition root: wires adapters to domain via ports.

This is the only file that knows all concrete types.
It creates instances, connects them, and starts the application.
No business logic belongs here.
"""

import sys
import tkinter as tk
from pathlib import Path

# Add project root to path so layer imports work
sys.path.insert(0, str(Path(__file__).parent))

from adapters.filesystem import LocalFileReader, LocalFileWriter
from adapters.tkinter_ui import EditorWindow
from application.use_cases import (
    OpenDocumentUseCase,
    SaveDocumentAsUseCase,
    SaveDocumentUseCase,
    UpdateContentUseCase,
)
from domain.model import Document, WindowState


def main() -> None:
    # Domain objects
    document = Document()
    window_state = WindowState()

    # Outgoing adapters (implement outgoing ports)
    reader = LocalFileReader()
    writer = LocalFileWriter()

    # Use cases (implement incoming ports, receive outgoing ports)
    open_doc = OpenDocumentUseCase(document, reader)
    save_doc = SaveDocumentUseCase(document, writer)
    save_doc_as = SaveDocumentAsUseCase(document, writer)
    update_content = UpdateContentUseCase(document)

    # Incoming adapter (tkinter UI drives use cases)
    root = tk.Tk()
    EditorWindow(
        root=root,
        document=document,
        window_state=window_state,
        open_doc=open_doc,
        save_doc=save_doc,
        save_doc_as=save_doc_as,
        update_content=update_content,
    )
    root.mainloop()


if __name__ == "__main__":
    main()
