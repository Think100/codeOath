"""Composition root: the only place that wires the concrete adapter
(``FileSystemPostRepository``) to the domain port and starts the app.

Run with: python -m blog.main
"""

from __future__ import annotations

import logging
from pathlib import Path

from blog.adapters.markdown_repository import FileSystemPostRepository
from blog.adapters.web import create_app

PROJECT_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = PROJECT_ROOT / "posts"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
STATIC_DIR = PROJECT_ROOT / "static"


def main() -> None:
    # Logging lives here, not in domain/, so business logic never decides
    # where or how to log.
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    repository = FileSystemPostRepository(POSTS_DIR)
    app = create_app(repository, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
    app.run(debug=True)


if __name__ == "__main__":
    main()
