"""Incoming adapter: tkinter GUI that drives the use cases.

This adapter translates user interactions into use case calls.
It knows about ports (incoming port types) and domain model, but
never performs business logic or file I/O itself.
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from application.use_cases import (
    OpenDocumentUseCase,
    SaveDocumentAsUseCase,
    SaveDocumentUseCase,
    UpdateContentUseCase,
)
from domain.model import Document, WindowState


class EditorWindow:
    """Main editor window. Translates GUI events into use case calls."""

    def __init__(
        self,
        root: tk.Tk,
        document: Document,
        window_state: WindowState,
        open_doc: OpenDocumentUseCase,
        save_doc: SaveDocumentUseCase,
        save_doc_as: SaveDocumentAsUseCase,
        update_content: UpdateContentUseCase,
    ) -> None:
        self._root = root
        self._document = document
        self._window_state = window_state
        self._open_doc = open_doc
        self._save_doc = save_doc
        self._save_doc_as = save_doc_as
        self._update_content = update_content

        self._build_ui()
        self._bind_events()
        self._update_title()

    # --- UI Construction ---

    def _build_ui(self) -> None:
        self._root.geometry("800x600")
        self._root.minsize(400, 300)

        # Toolbar frame
        toolbar = tk.Frame(self._root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(toolbar, text="Open", command=self._on_open).pack(
            side=tk.LEFT, padx=2, pady=2
        )
        tk.Button(toolbar, text="Save", command=self._on_save).pack(
            side=tk.LEFT, padx=2, pady=2
        )
        tk.Button(toolbar, text="Save As", command=self._on_save_as).pack(
            side=tk.LEFT, padx=2, pady=2
        )

        # Separator
        tk.Frame(toolbar, width=20).pack(side=tk.LEFT)

        # Always-on-top toggle
        self._on_top_var = tk.BooleanVar(value=self._window_state.always_on_top)
        tk.Checkbutton(
            toolbar,
            text="Always on Top",
            variable=self._on_top_var,
            command=self._on_toggle_always_on_top,
        ).pack(side=tk.LEFT, padx=2, pady=2)

        # Separator
        tk.Frame(toolbar, width=20).pack(side=tk.LEFT)

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
        self._root.bind("<Control-s>", lambda e: self._on_save())
        self._root.bind("<Control-o>", lambda e: self._on_open())
        self._text.bind("<<Modified>>", self._on_text_modified)

    # --- Event Handlers (translate GUI events to use case calls) ---

    def _on_open(self) -> None:
        path_str = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path_str:
            return
        try:
            self._open_doc.execute(Path(path_str))
            self._text.delete("1.0", tk.END)
            self._text.insert("1.0", self._document.content)
            self._text.edit_modified(False)
            self._update_title()
        except OSError as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def _on_save(self) -> None:
        if self._document.file_path is None:
            self._on_save_as()
            return
        self._sync_content()
        try:
            self._save_doc.execute()
            self._text.edit_modified(False)
            self._update_title()
        except OSError as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

    def _on_save_as(self) -> None:
        path_str = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path_str:
            return
        self._sync_content()
        try:
            self._save_doc_as.execute(Path(path_str))
            self._text.edit_modified(False)
            self._update_title()
        except OSError as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

    def _on_toggle_always_on_top(self) -> None:
        self._window_state.toggle_always_on_top()
        self._root.attributes("-topmost", self._window_state.always_on_top)

    def _on_opacity_change(self, value: str) -> None:
        percent = int(value)
        self._window_state.set_opacity(percent / 100.0)
        self._root.attributes("-alpha", self._window_state.opacity)
        self._opacity_label.config(text=f"{percent}%")

    def _on_text_modified(self, _event: tk.Event) -> None:  # type: ignore[type-arg]
        if self._text.edit_modified():
            self._sync_content()
            self._update_title()
            self._text.edit_modified(False)

    # --- Internal Helpers ---

    def _sync_content(self) -> None:
        """Push current editor text into the domain model via use case."""
        content = self._text.get("1.0", f"{tk.END}-1c")
        self._update_content.execute(content)

    def _update_title(self) -> None:
        modified_marker = " *" if self._document.is_modified else ""
        self._root.title(f"{self._document.title}{modified_marker} - codeOath Editor")
