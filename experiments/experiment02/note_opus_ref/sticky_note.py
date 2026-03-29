"""
Sticky Note - a minimal always-on-top note-taking app.

Features:
- Auto-saves on every keystroke (debounced) and on close.
- Always-on-top toggle.
- Window transparency slider.
- Persists content to a local JSON file next to the script.
"""

from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path

SAVE_FILE = Path(__file__).with_name("note_data.json")
AUTOSAVE_DELAY_MS = 500  # debounce interval


class StickyNote:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Sticky Note")
        self.root.geometry("380x420")
        self.root.minsize(260, 200)
        self.root.attributes("-topmost", True)

        self._autosave_id: str | None = None
        self._build_ui()
        self._load()

    # ------------------------------------------------------------------ UI

    def _build_ui(self) -> None:
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=6, pady=(6, 0))

        # Always-on-top toggle
        self._topmost_var = tk.BooleanVar(value=True)
        self._pin_btn = tk.Checkbutton(
            toolbar,
            text="Pin on top",
            variable=self._topmost_var,
            command=self._toggle_topmost,
        )
        self._pin_btn.pack(side=tk.LEFT)

        # Transparency slider
        tk.Label(toolbar, text="Opacity:").pack(side=tk.LEFT, padx=(12, 4))
        self._opacity_var = tk.DoubleVar(value=1.0)
        self._opacity_slider = tk.Scale(
            toolbar,
            from_=0.3,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            variable=self._opacity_var,
            command=self._change_opacity,
            showvalue=False,
            length=120,
        )
        self._opacity_slider.pack(side=tk.LEFT)

        # Text area with scrollbar
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", 11),
            yscrollcommand=scrollbar.set,
        )
        self.text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text.yview)

        # Status bar
        self._status = tk.Label(
            self.root, text="", anchor=tk.W, fg="grey", font=("Segoe UI", 8)
        )
        self._status.pack(fill=tk.X, padx=8, pady=(0, 4))

        # Bindings
        self.text.bind("<<Modified>>", self._on_modified)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # -------------------------------------------------------------- actions

    def _toggle_topmost(self) -> None:
        on_top = self._topmost_var.get()
        self.root.attributes("-topmost", on_top)

    def _change_opacity(self, _event: str | None = None) -> None:
        self.root.attributes("-alpha", self._opacity_var.get())

    def _on_modified(self, _event: tk.Event | None = None) -> None:
        # tkinter fires <<Modified>> once, then we must reset the flag
        if not self.text.edit_modified():
            return
        self.text.edit_modified(False)
        self._schedule_autosave()

    def _schedule_autosave(self) -> None:
        if self._autosave_id is not None:
            self.root.after_cancel(self._autosave_id)
        self._autosave_id = self.root.after(AUTOSAVE_DELAY_MS, self._save)

    # --------------------------------------------------------- persistence

    def _save(self) -> None:
        data = {
            "content": self.text.get("1.0", tk.END).rstrip("\n"),
            "opacity": self._opacity_var.get(),
            "topmost": self._topmost_var.get(),
            "geometry": self.root.geometry(),
        }
        SAVE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        self._status.config(text="saved")
        # Clear the status after a moment
        self.root.after(2000, lambda: self._status.config(text=""))

    def _load(self) -> None:
        if not SAVE_FILE.exists():
            return
        try:
            data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return

        if content := data.get("content"):
            self.text.insert("1.0", content)
            self.text.edit_modified(False)

        if "opacity" in data:
            self._opacity_var.set(data["opacity"])
            self._change_opacity()

        if "topmost" in data:
            self._topmost_var.set(data["topmost"])
            self._toggle_topmost()

        if "geometry" in data:
            self.root.geometry(data["geometry"])

    # ---------------------------------------------------------------- lifecycle

    def _on_close(self) -> None:
        self._save()
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    StickyNote().run()
