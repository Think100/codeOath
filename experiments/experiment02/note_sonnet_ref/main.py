"""Entry point for Quick Note."""

import tkinter as tk

from note_app import NoteApp


def main() -> None:
    root = tk.Tk()
    NoteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
