"""
Simple tkinter text editor with always-on-top toggle and transparency slider.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path


class TextEditor:
    """Main application class for the text editor."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("800x600")

        # Track the currently open file path
        self.current_file: Path | None = None
        # Track unsaved changes
        self.modified = False
        # Track always-on-top state
        self.always_on_top = False

        self._build_menu()
        self._build_toolbar()
        self._build_editor()
        self._bind_shortcuts()

    # ---------- UI construction ----------

    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)

        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def _build_toolbar(self) -> None:
        """Build the top toolbar with always-on-top toggle and transparency slider."""
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Always-on-top toggle button
        self.aot_btn = tk.Button(
            toolbar,
            text="Pin: OFF",
            width=9,
            command=self._toggle_always_on_top,
        )
        self.aot_btn.pack(side=tk.LEFT, padx=4)

        # Separator label
        tk.Label(toolbar, text="|").pack(side=tk.LEFT, padx=2)

        # Transparency label + slider
        tk.Label(toolbar, text="Opacity:").pack(side=tk.LEFT, padx=(8, 2))
        self.opacity_var = tk.DoubleVar(value=1.0)
        opacity_slider = tk.Scale(
            toolbar,
            variable=self.opacity_var,
            from_=0.2,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            length=160,
            showvalue=False,
            command=self._on_opacity_change,
        )
        opacity_slider.pack(side=tk.LEFT, padx=2)

        # Numeric readout for opacity
        self.opacity_label = tk.Label(toolbar, text="100%", width=5)
        self.opacity_label.pack(side=tk.LEFT)

    def _build_editor(self) -> None:
        """Build the main text area with scrollbars and a status bar."""
        # Status bar at the bottom
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor=tk.W,
            bd=1,
            relief=tk.SUNKEN,
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Scrollable text widget
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.text = tk.Text(
            frame,
            wrap=tk.NONE,
            undo=True,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            font=("Consolas", 11),
        )
        self.text.pack(fill=tk.BOTH, expand=True)

        scrollbar_y.config(command=self.text.yview)
        scrollbar_x.config(command=self.text.xview)

        # Detect modifications to show unsaved indicator in title
        self.text.bind("<<Modified>>", self._on_text_modified)

    def _bind_shortcuts(self) -> None:
        self.root.bind("<Control-o>", lambda _e: self.open_file())
        self.root.bind("<Control-s>", lambda _e: self.save_file())
        self.root.bind("<Control-S>", lambda _e: self.save_file_as())
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------- File operations ----------

    def open_file(self) -> None:
        if not self._confirm_discard():
            return

        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return

        self.current_file = Path(path)
        try:
            content = self.current_file.read_text(encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Open Error", str(exc))
            return

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
        # Reset the internal modified flag after loading
        self.text.edit_modified(False)
        self._set_modified(False)
        self._update_title()
        self.status_var.set(f"Opened: {self.current_file}")

    def save_file(self) -> bool:
        """Save to the current file; falls back to Save As if no file is open."""
        if self.current_file is None:
            return self.save_file_as()
        return self._write_file(self.current_file)

    def save_file_as(self) -> bool:
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return False
        self.current_file = Path(path)
        return self._write_file(self.current_file)

    def _write_file(self, path: Path) -> bool:
        content = self.text.get("1.0", tk.END)
        # tk always appends a trailing newline; strip one trailing newline to avoid
        # accumulating extra blank lines on each save cycle.
        if content.endswith("\n"):
            content = content[:-1]
        try:
            path.write_text(content, encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Save Error", str(exc))
            return False

        self.text.edit_modified(False)
        self._set_modified(False)
        self._update_title()
        self.status_var.set(f"Saved: {path}")
        return True

    # ---------- Window behavior ----------

    def _toggle_always_on_top(self) -> None:
        self.always_on_top = not self.always_on_top
        self.root.wm_attributes("-topmost", self.always_on_top)
        self.aot_btn.config(text=f"Pin: {'ON ' if self.always_on_top else 'OFF'}")

    def _on_opacity_change(self, _value: str) -> None:
        opacity = self.opacity_var.get()
        self.root.wm_attributes("-alpha", opacity)
        self.opacity_label.config(text=f"{int(opacity * 100)}%")

    # ---------- State helpers ----------

    def _on_text_modified(self, _event: tk.Event) -> None:
        # The <<Modified>> virtual event fires even when we reset it programmatically,
        # so only act when the flag is actually set.
        if self.text.edit_modified():
            self._set_modified(True)

    def _set_modified(self, value: bool) -> None:
        self.modified = value
        self._update_title()

    def _update_title(self) -> None:
        name = self.current_file.name if self.current_file else "Untitled"
        indicator = " *" if self.modified else ""
        self.root.title(f"{name}{indicator} - Text Editor")

    def _confirm_discard(self) -> bool:
        """Return True if it is safe to discard current content."""
        if not self.modified:
            return True
        answer = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes. Discard them?",
        )
        # None means Cancel, False means No (don't discard)
        return answer is True

    def _on_close(self) -> None:
        if self._confirm_discard():
            self.root.destroy()


def main() -> None:
    root = tk.Tk()
    TextEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
