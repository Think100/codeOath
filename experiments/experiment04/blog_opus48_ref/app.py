"""A simple Markdown blog system.

Posts are written as Markdown files in the ``posts/`` directory. Each file
starts with a YAML front matter block that carries the metadata::

    ---
    title: My First Post
    date: 2026-07-01
    tags: [python, web]
    ---

    The body of the post, written in **Markdown**.

The application renders every post to HTML, lists them newest first on the
home page, and serves a dedicated page for each post.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter
import markdown
from flask import Flask, abort, render_template

# Directory that holds the Markdown source files.
POSTS_DIR = Path(__file__).resolve().parent / "posts"

# Markdown extensions: fenced code blocks, syntax highlighting, tables and
# table-of-contents style anchors. These cover the common cases without
# needing per-post configuration.
MARKDOWN_EXTENSIONS = ["fenced_code", "codehilite", "tables", "sane_lists"]

app = Flask(__name__)


@dataclass
class Post:
    """A single blog post loaded from a Markdown file."""

    slug: str
    title: str
    date: dt.date
    tags: list[str] = field(default_factory=list)
    html: str = ""

    @property
    def date_display(self) -> str:
        """Human-readable date, e.g. ``July 01, 2026``."""
        return self.date.strftime("%B %d, %Y")

    @property
    def date_iso(self) -> str:
        """Machine-readable date for the ``<time>`` element."""
        return self.date.isoformat()


def _parse_date(value: object) -> dt.date:
    """Coerce a front matter date value into a ``datetime.date``.

    PyYAML parses unquoted ISO dates into ``date`` objects already, but a
    quoted or otherwise unusual value arrives as a string, so we handle both.
    Posts without a valid date fall back to the epoch so they sort last rather
    than crashing the whole site.
    """
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value.strip())
        except ValueError:
            pass
    return dt.date.min


def _parse_tags(value: object) -> list[str]:
    """Normalise the ``tags`` field into a list of strings.

    Accepts a YAML list (``[a, b]``) or a comma-separated string (``a, b``).
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [tag.strip() for tag in value.split(",") if tag.strip()]
    if isinstance(value, (list, tuple)):
        return [str(tag).strip() for tag in value if str(tag).strip()]
    return [str(value).strip()]


def load_post(path: Path) -> Post:
    """Load and render a single Markdown file into a :class:`Post`."""
    document = frontmatter.load(path)
    # A fresh converter per call keeps rendering isolated (the codehilite and
    # toc extensions carry per-document state).
    renderer = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    html = renderer.convert(document.content)

    return Post(
        slug=path.stem,
        title=str(document.get("title", path.stem)),
        date=_parse_date(document.get("date")),
        tags=_parse_tags(document.get("tags")),
        html=html,
    )


def load_posts() -> list[Post]:
    """Load every post, sorted newest first.

    Posts are read from disk on each request. For a small local blog this keeps
    things simple and means edits show up on refresh without a restart.
    """
    if not POSTS_DIR.is_dir():
        return []

    posts = [load_post(path) for path in POSTS_DIR.glob("*.md")]
    posts.sort(key=lambda post: (post.date, post.slug), reverse=True)
    return posts


@app.route("/")
def index():
    """Home page: list all posts, newest first."""
    return render_template("index.html", posts=load_posts())


@app.route("/posts/<slug>/")
def post_detail(slug: str):
    """Detail page for a single post."""
    for post in load_posts():
        if post.slug == slug:
            return render_template("post.html", post=post)
    abort(404)


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Debug mode enables auto-reload and readable error pages, which is what
    # you want while writing posts locally.
    app.run(host="127.0.0.1", port=5000, debug=True)
