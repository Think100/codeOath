"""
Quick Note -- a minimal always-on-top sticky note with autosave and opacity control.

Single persistent note stored in note.txt next to this file.
No open/save dialogs: the file is written automatically after every edit pause.
"""

import tkinter as tk
from pathlib import Path

import config


class NoteApp:
    """Main application window."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(config.APP_TITLE)
        self.root.geometry(config.DEFAULT_WINDOW_SIZE)

        self._always_on_top = False
        # Pending autosave callback id; None when no save is scheduled.
        self._autosave_id: str | None = None

        self._build_toolbar()
        self._build_text_area()
        self._load_note()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_toolbar(self) -> None:
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Pin / always-on-top toggle
        self._pin_btn = tk.Button(
            toolbar,
            text="Pin: OFF",
            width=8,
            command=self._toggle_pin,
        )
        self._pin_btn.pack(side=tk.LEFT, padx=4)

        tk.Label(toolbar, text="|").pack(side=tk.LEFT, padx=2)

        # Opacity slider
        tk.Label(toolbar, text="Opacity:").pack(side=tk.LEFT, padx=(6, 2))
        self._opacity_var = tk.DoubleVar(value=config.DEFAULT_OPACITY)
        tk.Scale(
            toolbar,
            variable=self._opacity_var,
            from_=config.MIN_OPACITY,
            to=config.MAX_OPACITY,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            length=140,
            showvalue=False,
            command=self._on_opacity_change,
        ).pack(side=tk.LEFT, padx=2)

        self._opacity_label = tk.Label(toolbar, text="100%", width=5)
        self._opacity_label.pack(side=tk.LEFT)

        # Status indicator (right-aligned)
        self._status_var = tk.StringVar(value="")
        tk.Label(toolbar, textvariable=self._status_var, fg="gray", anchor=tk.E).pack(
            side=tk.RIGHT, padx=6
        )

    def _build_text_area(self) -> None:
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._text = tk.Text(
            frame,
            wrap=tk.WORD,
            undo=True,
            yscrollcommand=scrollbar.set,
            font=config.FONT,
            padx=6,
            pady=6,
        )
        self._text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._text.yview)

        # Schedule autosave on every keystroke / edit
        self._text.bind("<<Modified>>", self._on_modified)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load_note(self) -> None:
        """Load the persisted note file if it exists."""
        path: Path = config.NOTE_FILE
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8")
            except OSError:
                content = ""
            self._text.insert("1.0", content)
            # Move cursor to end so the user can continue typing immediately
            self._text.mark_set(tk.INSERT, tk.END)
            self._text.see(tk.INSERT)
        # Reset the internal modified flag so the first load does not trigger a save
        self._text.edit_modified(False)

    def _save_note(self) -> None:
        """Write the current content to disk immediately."""
        content = self._text.get("1.0", tk.END)
        # tk always appends a trailing newline; strip exactly one to avoid
        # accumulating blank lines across save cycles.
        if content.endswith("\n"):
            content = content[:-1]
        try:
            config.NOTE_FILE.write_text(content, encoding="utf-8")
            self._status_var.set("Saved")
            # Clear the "Saved" message after 2 s so it does not distract
            self.root.after(2_000, lambda: self._status_var.set(""))
        except OSError as exc:
            self._status_var.set(f"Save error: {exc}")

    def _schedule_autosave(self) -> None:
        """Reset the autosave timer. Called after every edit."""
        if self._autosave_id is not None:
            self.root.after_cancel(self._autosave_id)
        self._autosave_id = self.root.after(config.AUTOSAVE_DELAY_MS, self._autosave)

    def _autosave(self) -> None:
        self._autosave_id = None
        self._save_note()
        # Reset the modified flag so subsequent unmodified events are ignored
        self._text.edit_modified(False)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_modified(self, _event: tk.Event) -> None:
        # <<Modified>> fires both when the user edits AND when we call
        # edit_modified(False) to reset the flag. Only act on real edits.
        if self._text.edit_modified():
            self._schedule_autosave()

    def _toggle_pin(self) -> None:
        self._always_on_top = not self._always_on_top
        self.root.wm_attributes("-topmost", self._always_on_top)
        self._pin_btn.config(text=f"Pin: {'ON ' if self._always_on_top else 'OFF'}")

    def _on_opacity_change(self, _value: str) -> None:
        opacity = self._opacity_var.get()
        self.root.wm_attributes("-alpha", opacity)
        self._opacity_label.config(text=f"{int(opacity * 100)}%")

    def _on_close(self) -> None:
        # Cancel any pending autosave and do a final synchronous save before exit.
        if self._autosave_id is not None:
            self.root.after_cancel(self._autosave_id)
        self._save_note()
        self.root.destroy()
