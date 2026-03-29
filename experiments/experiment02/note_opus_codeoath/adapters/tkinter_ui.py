"""Incoming adapter: tkinter GUI that drives the use cases.

This adapter translates user interactions into use case calls.
It knows about ports (incoming port types) and domain model, but
never performs business logic or file I/O itself.
"""

import tkinter as tk

from application.use_cases import (
    LoadNoteUseCase,
    SaveNoteUseCase,
    UpdateNoteUseCase,
)
from domain.model import Note, WindowState

# Auto-save fires this many milliseconds after the last keystroke
_AUTOSAVE_DELAY_MS = 1000


class NoteWindow:
    """Main note window. Translates GUI events into use case calls."""

    def __init__(
        self,
        root: tk.Tk,
        note: Note,
        window_state: WindowState,
        load_note: LoadNoteUseCase,
        save_note: SaveNoteUseCase,
        update_note: UpdateNoteUseCase,
    ) -> None:
        self._root = root
        self._note = note
        self._window_state = window_state
        self._load_note = load_note
        self._save_note = save_note
        self._update_note = update_note
        self._autosave_id: str | None = None

        self._build_ui()
        self._bind_events()
        self._load_existing_note()

    # --- UI Construction ---

    def _build_ui(self) -> None:
        self._root.title("Quick Note")
        self._root.geometry("420x500")
        self._root.minsize(300, 200)

        # Toolbar frame
        toolbar = tk.Frame(self._root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Always-on-top toggle
        self._on_top_var = tk.BooleanVar(value=self._window_state.always_on_top)
        tk.Checkbutton(
            toolbar,
            text="Pin on Top",
            variable=self._on_top_var,
            command=self._on_toggle_always_on_top,
        ).pack(side=tk.LEFT, padx=4, pady=2)

        # Separator
        tk.Frame(toolbar, width=12).pack(side=tk.LEFT)

        # Opacity slider
        tk.Label(toolbar, text="Opacity:").pack(side=tk.LEFT, padx=(2, 0))
        self._opacity_scale = tk.Scale(
            toolbar,
            from_=10,
            to=100,
            orient=tk.HORIZONTAL,
            length=120,
            showvalue=False,
            command=self._on_opacity_change,
        )
        self._opacity_scale.set(int(self._window_state.opacity * 100))
        self._opacity_scale.pack(side=tk.LEFT, padx=2, pady=2)

        self._opacity_label = tk.Label(toolbar, text="100%", width=5)
        self._opacity_label.pack(side=tk.LEFT)

        # Status label (right-aligned)
        self._status_label = tk.Label(
            toolbar, text="", fg="gray", anchor=tk.E
        )
        self._status_label.pack(side=tk.RIGHT, padx=6)

        # Text area with scrollbar
        text_frame = tk.Frame(self._root)
        text_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", 11),
            yscrollcommand=scrollbar.set,
        )
        self._text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._text.yview)

    def _bind_events(self) -> None:
        self._text.bind("<<Modified>>", self._on_text_modified)
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

    # --- Load Existing Note ---

    def _load_existing_note(self) -> None:
        """Load persisted note content into the text widget."""
        self._load_note.execute()
        if self._note.content:
            self._text.insert("1.0", self._note.content)
            self._text.edit_modified(False)

    # --- Event Handlers ---

    def _on_text_modified(self, _event: tk.Event) -> None:  # type: ignore[type-arg]
        if not self._text.edit_modified():
            return
        self._sync_content()
        self._text.edit_modified(False)
        self._schedule_autosave()

    def _on_toggle_always_on_top(self) -> None:
        self._window_state.toggle_always_on_top()
        self._root.attributes("-topmost", self._window_state.always_on_top)

    def _on_opacity_change(self, value: str) -> None:
        percent = int(value)
        self._window_state.set_opacity(percent / 100.0)
        self._root.attributes("-alpha", self._window_state.opacity)
        self._opacity_label.config(text=f"{percent}%")

    def _on_close(self) -> None:
        """Save before exiting."""
        self._sync_content()
        self._save_note.execute()
        self._root.destroy()

    # --- Auto-Save ---

    def _schedule_autosave(self) -> None:
        """Reset the auto-save timer. Fires after a pause in typing."""
        if self._autosave_id is not None:
            self._root.after_cancel(self._autosave_id)
        self._autosave_id = self._root.after(
            _AUTOSAVE_DELAY_MS, self._do_autosave
        )

    def _do_autosave(self) -> None:
        self._autosave_id = None
        self._save_note.execute()
        self._flash_status("saved")

    def _flash_status(self, text: str) -> None:
        """Briefly show a status message, then clear it."""
        self._status_label.config(text=text)
        self._root.after(2000, lambda: self._status_label.config(text=""))

    # --- Internal Helpers ---

    def _sync_content(self) -> None:
        """Push current editor text into the domain model via use case."""
        content = self._text.get("1.0", f"{tk.END}-1c")
        self._update_note.execute(content)
