# Blog System - Main Entry Point
#
# How to run:
#   1. Install dependencies:  pip install flask markdown
#   2. Start the server:      python main.py
#   3. Open in browser:       http://localhost:5000
#
# Posts are loaded from the posts/ directory. Each .md file with valid
# front-matter (title, date, optional tags) becomes a blog post.

from __future__ import annotations

import os
import sys

# Ensure the project root is on the Python path so that 'src' imports work.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.domain.service import BlogService
from src.infrastructure.file_repository import FilePostRepository
from src.infrastructure.markdown_renderer import PythonMarkdownRenderer
from src.infrastructure.web import create_app


def main() -> None:
    posts_dir = os.path.join(PROJECT_ROOT, "posts")

    # Wire up infrastructure adapters
    repository = FilePostRepository(posts_dir)
    renderer = PythonMarkdownRenderer()

    # Create domain service
    blog_service = BlogService(repository=repository, renderer=renderer)

    # Create and run the web app
    app = create_app(blog_service)
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
