"""Composition root: wires the file repository into the web app and serves it.

Run with:  python app.py  (then open http://127.0.0.1:5000)
"""

from pathlib import Path

from src.adapters.file_repository import FileSystemPostRepository
from src.adapters.web import create_app

POSTS_DIR = Path(__file__).parent / "posts"

app = create_app(FileSystemPostRepository(posts_dir=POSTS_DIR))

if __name__ == "__main__":
    # Local dev server only, bound to localhost on purpose (see AGENTS.md NOT).
    app.run(host="127.0.0.1", port=5000, debug=False)
