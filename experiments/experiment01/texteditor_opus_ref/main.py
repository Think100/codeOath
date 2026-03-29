"""Entry point for the codeOath Texteditor."""

import tkinter as tk

from editor import TextEditor


def main() -> None:
    root = tk.Tk()
    TextEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
