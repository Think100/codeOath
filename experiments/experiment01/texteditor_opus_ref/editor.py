"""Core editor window built with tkinter."""

import tkinter as tk
from tkinter import filedialog, messagebox

from config import (
    APP_TITLE,
    DEFAULT_OPACITY,
    DEFAULT_WINDOW_SIZE,
    FILE_TYPES,
    MAX_OPACITY,
    MIN_OPACITY,
)


class TextEditor:
    """Simple text editor with always-on-top and transparency controls."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.current_file: str | None = None
        self._topmost = False

        self._setup_window()
        self._create_menu()
        self._create_toolbar()
        self._create_text_area()
        self._bind_shortcuts()

    # ── Window setup ────────────────────────────────────────────

    def _setup_window(self) -> None:
        self.root.title(APP_TITLE)
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        self.root.attributes("-alpha", DEFAULT_OPACITY)

    # ── Menu bar ────────────────────────────────────────────────

    def _create_menu(self) -> None:
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open...", command=self._open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self._save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self._save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menubar)

    # ── Toolbar with always-on-top toggle and transparency slider ──

    def _create_toolbar(self) -> None:
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Always-on-top toggle
        self._topmost_var = tk.BooleanVar(value=False)
        topmost_cb = tk.Checkbutton(
            toolbar,
            text="Always on Top",
            variable=self._topmost_var,
            command=self._toggle_topmost,
        )
        topmost_cb.pack(side=tk.LEFT, padx=6, pady=2)

        # Separator
        tk.Label(toolbar, text="|").pack(side=tk.LEFT, padx=4)

        # Transparency slider
        tk.Label(toolbar, text="Opacity:").pack(side=tk.LEFT, padx=(6, 2))
        self._opacity_slider = tk.Scale(
            toolbar,
            from_=int(MIN_OPACITY * 100),
            to=int(MAX_OPACITY * 100),
            orient=tk.HORIZONTAL,
            length=150,
            showvalue=False,
            command=self._on_opacity_change,
        )
        self._opacity_slider.set(int(DEFAULT_OPACITY * 100))
        self._opacity_slider.pack(side=tk.LEFT, padx=2, pady=2)

        self._opacity_label = tk.Label(toolbar, text="100%", width=5)
        self._opacity_label.pack(side=tk.LEFT)

    # ── Text area ───────────────────────────────────────────────

    def _create_text_area(self) -> None:
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text = tk.Text(
            frame,
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", 11),
            yscrollcommand=scrollbar.set,
        )
        self.text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text.yview)

    # ── Keyboard shortcuts ──────────────────────────────────────

    def _bind_shortcuts(self) -> None:
        self.root.bind("<Control-o>", lambda _: self._open_file())
        self.root.bind("<Control-s>", lambda _: self._save_file())
        self.root.bind("<Control-Shift-S>", lambda _: self._save_file_as())

    # ── File operations ─────────────────────────────────────────

    def _open_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=FILE_TYPES)
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")
            return

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
        self.current_file = path
        self._update_title()

    def _save_file(self) -> None:
        if self.current_file is None:
            self._save_file_as()
            return
        self._write_file(self.current_file)

    def _save_file_as(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=FILE_TYPES,
        )
        if not path:
            return
        self._write_file(path)
        self.current_file = path
        self._update_title()

    def _write_file(self, path: str) -> None:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", tk.END).rstrip("\n"))
        except OSError as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

    # ── Toolbar callbacks ───────────────────────────────────────

    def _toggle_topmost(self) -> None:
        self._topmost = self._topmost_var.get()
        self.root.attributes("-topmost", self._topmost)

    def _on_opacity_change(self, value: str) -> None:
        percent = int(value)
        self.root.attributes("-alpha", percent / 100)
        self._opacity_label.config(text=f"{percent}%")

    # ── Helpers ─────────────────────────────────────────────────

    def _update_title(self) -> None:
        name = self.current_file or "Untitled"
        self.root.title(f"{name} - {APP_TITLE}")
