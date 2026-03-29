"""
ui.py -- tkinter adapter. Outer ring.

This file implements the EditorPort contract from app.py.
It is the ONLY file in this project that may touch tkinter.

Dependency direction: ui.py -> app.py -> domain.py
                      (always inward, never reversed)

Rule: This file may import tkinter, app, and domain (read-only for types).
      Domain objects are treated as values here; we never mutate them.
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from app import EditorApplication, EditorPort
from domain import WindowSettings


# Colour palette -- centralised so the toolbar and text area stay consistent.
_DARK_BG = "#1e1e1e"
_TOOLBAR_BG = "#2d2d2d"
_STATUSBAR_BG = "#007acc"
_FG = "#d4d4d4"
_BUTTON_BG = "#3c3c3c"
_BUTTON_ACTIVE = "#505050"
_ACCENT_ON = "#0e7e12"    # green -- always-on-top active
_ACCENT_OFF = "#3c3c3c"   # default button -- always-on-top inactive
_FONT_MONO = ("Consolas", 11)
_FONT_UI = ("Segoe UI", 9)


class EditorWindow(EditorPort):
    """tkinter window that satisfies the EditorPort contract.

    Implements every method the application layer may call back through.
    Keeps all tkinter widgets private; nothing outside this class touches them.
    """

    def __init__(self, app: EditorApplication) -> None:
        self._app = app
        self._root = tk.Tk()
        self._root.geometry("900x650")
        self._root.configure(bg=_DARK_BG)

        self._on_top_button: tk.Button
        self._text: tk.Text
        self._status_var = tk.StringVar(value="Ready")

        self._build_toolbar()
        self._build_text_area()
        self._build_status_bar()
        self._bind_shortcuts()

        # Register ourselves as the UI implementation AFTER building widgets,
        # so the first _push_state() can safely call our methods.
        self._app.register_ui(self)

    def run(self) -> None:
        """Start the tkinter event loop. Blocks until the window is closed."""
        self._root.mainloop()

    # --- EditorPort implementation ---
    # These are the ONLY methods the application layer is allowed to call.

    def refresh_title(self, title: str) -> None:
        self._root.title(title)

    def refresh_content(self, content: str) -> None:
        """Replace the text widget contents without triggering the modify callback."""
        # Temporarily unbind <<Modified>> to avoid a feedback loop:
        # setting content would fire the event, which calls update_content,
        # which calls refresh_title -- an infinite cycle on open/load.
        self._text.unbind("<<Modified>>")
        self._text.delete("1.0", tk.END)
        self._text.insert("1.0", content)
        self._text.edit_modified(False)
        self._text.bind("<<Modified>>", self._on_text_modified)
        self._status_var.set("File loaded")

    def apply_window_settings(self, settings: WindowSettings) -> None:
        self._root.attributes("-topmost", settings.always_on_top)
        self._root.attributes("-alpha", settings.alpha)
        # Reflect always-on-top state visually on the button.
        color = _ACCENT_ON if settings.always_on_top else _ACCENT_OFF
        self._on_top_button.configure(bg=color)

    def show_error(self, message: str) -> None:
        messagebox.showerror("Error", message, parent=self._root)
        self._status_var.set(f"Error: {message}")

    def show_info(self, message: str) -> None:
        self._status_var.set(message)

    def ask_save_path(self) -> Path | None:
        raw = filedialog.asksaveasfilename(
            parent=self._root,
            title="Save File As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        return Path(raw) if raw else None

    def ask_open_path(self) -> Path | None:
        raw = filedialog.askopenfilename(
            parent=self._root,
            title="Open File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        return Path(raw) if raw else None

    # --- Private: widget construction ---

    def _build_toolbar(self) -> None:
        toolbar = tk.Frame(self._root, bg=_TOOLBAR_BG, pady=4)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        def btn(text: str, command, width: int = 8) -> tk.Button:
            return tk.Button(
                toolbar,
                text=text,
                command=command,
                bg=_BUTTON_BG,
                fg=_FG,
                activebackground=_BUTTON_ACTIVE,
                activeforeground=_FG,
                relief=tk.FLAT,
                font=_FONT_UI,
                width=width,
                cursor="hand2",
                bd=0,
                padx=6,
                pady=4,
            )

        btn("Open", self._app.open_file).pack(side=tk.LEFT, padx=(8, 2))
        btn("Save", self._app.save_file).pack(side=tk.LEFT, padx=2)
        btn("Save As", self._app.save_file_as, width=9).pack(side=tk.LEFT, padx=2)

        # Vertical separator
        tk.Frame(toolbar, bg="#555555", width=1).pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=2)

        # Always-on-top toggle -- we keep a reference to update its colour.
        self._on_top_button = btn("Pin", self._app.toggle_always_on_top, width=6)
        self._on_top_button.pack(side=tk.LEFT, padx=2)

        # Transparency controls on the right side.
        tk.Frame(toolbar, bg="#555555", width=1).pack(side=tk.RIGHT, fill=tk.Y, padx=8, pady=2)

        self._alpha_label = tk.Label(
            toolbar, text="100%", bg=_TOOLBAR_BG, fg=_FG, font=_FONT_UI, width=4
        )
        self._alpha_label.pack(side=tk.RIGHT, padx=(0, 6))

        tk.Label(toolbar, text="Opacity", bg=_TOOLBAR_BG, fg=_FG, font=_FONT_UI).pack(
            side=tk.RIGHT, padx=(0, 4)
        )

        alpha_slider = tk.Scale(
            toolbar,
            from_=10,
            to=100,
            orient=tk.HORIZONTAL,
            command=self._on_alpha_changed,
            bg=_TOOLBAR_BG,
            fg=_FG,
            highlightthickness=0,
            troughcolor="#555555",
            length=120,
            showvalue=False,
            sliderlength=14,
        )
        alpha_slider.set(100)
        alpha_slider.pack(side=tk.RIGHT, padx=(0, 4))

    def _build_text_area(self) -> None:
        frame = tk.Frame(self._root, bg=_DARK_BG)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, bg=_TOOLBAR_BG, troughcolor=_DARK_BG)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._text = tk.Text(
            frame,
            font=_FONT_MONO,
            bg=_DARK_BG,
            fg=_FG,
            insertbackground=_FG,
            selectbackground="#264f78",
            selectforeground=_FG,
            wrap=tk.NONE,
            undo=True,
            maxundo=-1,
            relief=tk.FLAT,
            bd=8,
            yscrollcommand=scrollbar.set,
        )
        self._text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._text.yview)

        self._text.bind("<<Modified>>", self._on_text_modified)

    def _build_status_bar(self) -> None:
        bar = tk.Frame(self._root, bg=_STATUSBAR_BG, height=22)
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        bar.pack_propagate(False)

        tk.Label(
            bar,
            textvariable=self._status_var,
            bg=_STATUSBAR_BG,
            fg="white",
            font=_FONT_UI,
            anchor="w",
        ).pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)

    # --- Private: event handlers ---

    def _bind_shortcuts(self) -> None:
        self._root.bind("<Control-s>", lambda _e: self._app.save_file() or "break")
        self._root.bind("<Control-S>", lambda _e: self._app.save_file_as() or "break")

    def _on_text_modified(self, _event: tk.Event) -> None:  # type: ignore[type-arg]
        """Called whenever the text widget content changes."""
        if not self._text.edit_modified():
            return
        content = self._text.get("1.0", tk.END)
        # Remove the trailing newline tkinter always appends.
        content = content.rstrip("\n")
        self._app.update_content(content)
        self._text.edit_modified(False)

    def _on_alpha_changed(self, value: str) -> None:
        """Slider callback. value is a string from tkinter."""
        percent = int(value)
        self._alpha_label.configure(text=f"{percent}%")
        self._app.set_alpha(percent / 100.0)
