#!/usr/bin/env python3
"""
main.py -- Entry point. Wires the layers together and starts the event loop.

Dependency graph (always inward):
  main -> ui -> app -> domain

This file's only job is composition: create the application, attach the UI,
hand control to the event loop. No business logic lives here.
"""

from app import EditorApplication
from ui import EditorWindow


def main() -> None:
    app = EditorApplication()
    window = EditorWindow(app)   # EditorWindow registers itself as the UI port
    window.run()


if __name__ == "__main__":
    main()
