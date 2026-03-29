"""
ui.py -- tkinter adapter. Outer ring.

Implements the NotePort contract from app.py.
This is the ONLY file in this project that may touch tkinter.

Dependency direction: ui.py -> app.py -> domain.py
                      (always inward, never reversed)

Rule: This file may import tkinter, app, and domain (read-only for types).
      Domain objects are treated as values here; we never mutate them.
"""

import tkinter as tk
from tkinter import messagebox

from app import NoteApplication, NotePort
from domain import WindowSettings


# Colour palette -- centralised so toolbar and text area stay consistent.
_BG = "#1e1e2e"          # main background
_TOOLBAR_BG = "#2a2a3d"  # slightly lighter for toolbar
_STATUSBAR_BG = "#313244"
_FG = "#cdd6f4"          # text colour
_BUTTON_BG = "#45475a"
_BUTTON_ACTIVE = "#585b70"
_ACCENT_ON = "#a6e3a1"   # green -- always-on-top active
_ACCENT_OFF = "#45475a"  # default -- always-on-top inactive
_FONT_TEXT = ("Segoe UI", 12)
_FONT_UI = ("Segoe UI", 9)

# Autosave interval in milliseconds.
# Short enough not to lose more than one second of work.
_AUTOSAVE_INTERVAL_MS = 1_000


class NoteWindow(NotePort):
    """tkinter window that satisfies the NotePort contract.

    Owns all widgets. The application layer calls back through the five
    NotePort methods; everything else is private to this class.
    """

    def __init__(self, app: NoteApplication) -> None:
        self._app = app
        self._root = tk.Tk()
        self._root.geometry("420x340")
        self._root.configure(bg=_BG)
        self._root.resizable(True, True)

        self._on_top_button: tk.Button
        self._text: tk.Text
        self._status_var = tk.StringVar(value="Ready")

        self._build_toolbar()
        self._build_text_area()
        self._build_status_bar()
        self._bind_close()

        # Register AFTER building widgets so the first _push_state()
        # and _load_persisted() can safely call our NotePort methods.
        self._app.register_ui(self)

        # Start the autosave timer after registration.
        self._schedule_autosave()

    def run(self) -> None:
        """Start the tkinter event loop. Blocks until the window is closed."""
        self._root.mainloop()

    # --- NotePort implementation ---
    # These are the ONLY methods the application layer is allowed to call.

    def refresh_title(self, title: str) -> None:
        self._root.title(title)

    def refresh_content(self, content: str) -> None:
        """Replace the text widget contents without triggering the modify callback.

        Temporarily unbind <<Modified>> to avoid a feedback loop:
        inserting content would fire the event -> update_content ->
        refresh_title -> infinite cycle.
        """
        self._text.unbind("<<Modified>>")
        self._text.delete("1.0", tk.END)
        self._text.insert("1.0", content)
        self._text.edit_modified(False)
        self._text.bind("<<Modified>>", self._on_text_modified)

    def apply_window_settings(self, settings: WindowSettings) -> None:
        self._root.attributes("-topmost", settings.always_on_top)
        self._root.attributes("-alpha", settings.alpha)
        color = _ACCENT_ON if settings.always_on_top else _ACCENT_OFF
        self._on_top_button.configure(bg=color, activebackground=color)

    def show_error(self, message: str) -> None:
        messagebox.showerror("Error", message, parent=self._root)
        self._status_var.set(f"Error: {message}")

    def show_status(self, message: str) -> None:
        self._status_var.set(message)

    # --- Private: widget construction ---

    def _build_toolbar(self) -> None:
        toolbar = tk.Frame(self._root, bg=_TOOLBAR_BG, pady=3)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Always-on-top toggle button.
        self._on_top_button = tk.Button(
            toolbar,
            text="Pin",
            command=self._app.toggle_always_on_top,
            bg=_ACCENT_ON,   # default: on-top is active
            fg=_BG,
            activeforeground=_BG,
            relief=tk.FLAT,
            font=_FONT_UI,
            width=5,
            cursor="hand2",
            bd=0,
            padx=6,
            pady=3,
        )
        self._on_top_button.pack(side=tk.LEFT, padx=(6, 2))

        # Opacity controls on the right.
        self._alpha_label = tk.Label(
            toolbar, text="100%", bg=_TOOLBAR_BG, fg=_FG, font=_FONT_UI, width=4
        )
        self._alpha_label.pack(side=tk.RIGHT, padx=(0, 6))

        tk.Label(toolbar, text="Opacity", bg=_TOOLBAR_BG, fg=_FG, font=_FONT_UI).pack(
            side=tk.RIGHT, padx=(0, 2)
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
            troughcolor=_BUTTON_BG,
            length=110,
            showvalue=False,
            sliderlength=14,
        )
        alpha_slider.set(100)
        alpha_slider.pack(side=tk.RIGHT, padx=(0, 4))

    def _build_text_area(self) -> None:
        frame = tk.Frame(self._root, bg=_BG)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, bg=_TOOLBAR_BG, troughcolor=_BG)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._text = tk.Text(
            frame,
            font=_FONT_TEXT,
            bg=_BG,
            fg=_FG,
            insertbackground=_FG,
            selectbackground="#585b70",
            selectforeground=_FG,
            wrap=tk.WORD,
            undo=True,
            maxundo=-1,
            relief=tk.FLAT,
            bd=10,
            yscrollcommand=scrollbar.set,
        )
        self._text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._text.yview)

        self._text.bind("<<Modified>>", self._on_text_modified)
        # Focus the text area immediately so the user can start typing.
        self._text.focus_set()

    def _build_status_bar(self) -> None:
        bar = tk.Frame(self._root, bg=_STATUSBAR_BG, height=20)
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        bar.pack_propagate(False)

        tk.Label(
            bar,
            textvariable=self._status_var,
            bg=_STATUSBAR_BG,
            fg=_FG,
            font=_FONT_UI,
            anchor="w",
        ).pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)

    def _bind_close(self) -> None:
        """Ensure a final save happens before the window is destroyed."""
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

    # --- Private: event handlers ---

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

    def _on_close(self) -> None:
        """Save immediately on close, then destroy the window."""
        self._app.save_now()
        self._root.destroy()

    def _schedule_autosave(self) -> None:
        """Arm the repeating autosave timer."""
        self._root.after(_AUTOSAVE_INTERVAL_MS, self._autosave_loop)

    def _autosave_loop(self) -> None:
        """Called by tkinter every _AUTOSAVE_INTERVAL_MS milliseconds.

        Delegates the save decision to the application layer.
        Rescheduling here (not in _schedule_autosave) keeps the loop alive
        even if save_tick raises -- tkinter's after() does not auto-repeat.
        """
        self._app.autosave_tick()
        self._root.after(_AUTOSAVE_INTERVAL_MS, self._autosave_loop)
