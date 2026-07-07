"""Simple file-based blog: Markdown posts rendered as HTML pages via Flask.

Posts live in the posts/ directory as .md files with a small front matter
block (title, date, optional tags). The filename (without extension) is the
URL slug, e.g. posts/hello-world.md -> /post/hello-world
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

import markdown
from flask import Flask, abort, render_template

BASE_DIR = Path(__file__).parent
POSTS_DIR = BASE_DIR / "posts"

app = Flask(__name__)


@dataclass
class Post:
    slug: str
    title: str
    date: date
    html: str
    tags: list[str] = field(default_factory=list)


class PostError(ValueError):
    """Raised when a post file cannot be parsed."""


def parse_front_matter(text: str, path: Path) -> tuple[dict[str, str], str]:
    """Split a post file into front matter metadata and Markdown body.

    Front matter is a block delimited by '---' lines at the top of the file,
    containing simple 'key: value' pairs.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise PostError(f"{path.name}: missing front matter (file must start with '---')")

    meta: dict[str, str] = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body = "\n".join(lines[i + 1:])
            return meta, body
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise PostError(f"{path.name}: invalid front matter line: {line!r}")
        meta[key.strip().lower()] = value.strip()

    raise PostError(f"{path.name}: front matter not closed (missing second '---')")


def load_post(path: Path) -> Post:
    """Parse a single Markdown file into a Post."""
    meta, body = parse_front_matter(path.read_text(encoding="utf-8"), path)

    if "title" not in meta or not meta["title"]:
        raise PostError(f"{path.name}: front matter is missing 'title'")
    if "date" not in meta:
        raise PostError(f"{path.name}: front matter is missing 'date'")
    try:
        post_date = datetime.strptime(meta["date"], "%Y-%m-%d").date()
    except ValueError:
        raise PostError(f"{path.name}: date must be YYYY-MM-DD, got {meta['date']!r}")

    tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    html = markdown.markdown(body, extensions=["fenced_code", "tables"])

    return Post(slug=path.stem, title=meta["title"], date=post_date, html=html, tags=tags)


def load_all_posts() -> list[Post]:
    """Load every post, newest first. Skips broken files with a warning."""
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        try:
            posts.append(load_post(path))
        except PostError as err:
            app.logger.warning("Skipping post: %s", err)
    posts.sort(key=lambda p: p.date, reverse=True)
    return posts


@app.route("/")
def index():
    return render_template("index.html", posts=load_all_posts())


@app.route("/post/<slug>")
def post(slug):
    path = POSTS_DIR / f"{slug}.md"
    # Guard against path traversal (e.g. slug containing '..') and missing files.
    if Path(slug).name != slug or not path.is_file():
        abort(404)
    try:
        return render_template("post.html", post=load_post(path))
    except PostError as err:
        app.logger.warning("Cannot render post: %s", err)
        abort(404)


@app.errorhandler(404)
def not_found(_err):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
