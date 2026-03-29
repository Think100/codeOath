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

from adapters.json_storage import JsonNoteStorage
from adapters.tkinter_ui import NoteWindow
from application.use_cases import (
    LoadNoteUseCase,
    SaveNoteUseCase,
    UpdateNoteUseCase,
)
from domain.model import Note, WindowState

# Store note data next to the script so it survives restarts
_DATA_FILE = Path(__file__).parent / "data" / "note.json"


def main() -> None:
    # Domain objects
    note = Note()
    window_state = WindowState()

    # Outgoing adapter (implements outgoing port)
    storage = JsonNoteStorage(_DATA_FILE)

    # Use cases (implement incoming ports, receive outgoing ports)
    load_note = LoadNoteUseCase(note, storage)
    save_note = SaveNoteUseCase(note, storage)
    update_note = UpdateNoteUseCase(note)

    # Incoming adapter (tkinter UI drives use cases)
    root = tk.Tk()
    NoteWindow(
        root=root,
        note=note,
        window_state=window_state,
        load_note=load_note,
        save_note=save_note,
        update_note=update_note,
    )
    root.mainloop()


if __name__ == "__main__":
    main()
