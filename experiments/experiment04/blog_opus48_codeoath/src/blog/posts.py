"""Loading and parsing blog posts from Markdown files.

A post is a ``.md`` file in the posts directory with a front matter header
delimited by ``---`` lines:

    ---
    title: My first post
    date: 2026-06-01
    tags: intro, meta
    ---

    Markdown body...

The file name without the ``.md`` extension is used as the URL slug.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from pathlib import Path

from .markdown import render_markdown


class PostError(ValueError):
    """Raised when a post file is malformed. Never swallowed silently."""


@dataclass(frozen=True)
class Post:
    """A single blog post, parsed from a Markdown file."""

    slug: str
    title: str
    date: _dt.date
    body_markdown: str
    tags: list[str] = field(default_factory=list)

    @property
    def html(self) -> str:
        """The rendered HTML body of the post."""
        return render_markdown(self.body_markdown)

    @property
    def date_display(self) -> str:
        """Human-readable date, e.g. '01 June 2026'."""
        return self.date.strftime("%d %B %Y")


def _split_front_matter(text: str) -> tuple[str, str]:
    """Split raw file text into (front matter, body).

    Raises PostError if the front matter block is missing or not closed.
    """
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---"):
        raise PostError("missing front matter (file must start with '---')")

    lines = normalized.split("\n")
    # lines[0] is the opening '---'. Find the closing '---'.
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            front = "\n".join(lines[1:index])
            body = "\n".join(lines[index + 1 :]).lstrip("\n")
            return front, body

    raise PostError("front matter is not closed (missing second '---')")


def _parse_front_matter(front: str) -> dict[str, str]:
    """Parse simple ``key: value`` front matter into a dict."""
    fields: dict[str, str] = {}
    for raw_line in front.split("\n"):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise PostError(f"invalid front matter line (no ':'): {raw_line!r}")
        key, value = line.split(":", 1)
        fields[key.strip().lower()] = value.strip()
    return fields


def _parse_tags(value: str) -> list[str]:
    """Parse a comma-separated tags string into a clean list."""
    return [tag.strip() for tag in value.split(",") if tag.strip()]


def parse_post(text: str, slug: str) -> Post:
    """Parse the raw contents of a post file into a Post."""
    front, body = _split_front_matter(text)
    fields = _parse_front_matter(front)

    title = fields.get("title", "").strip()
    if not title:
        raise PostError("missing required field 'title'")

    date_value = fields.get("date", "").strip()
    if not date_value:
        raise PostError("missing required field 'date'")
    try:
        date = _dt.date.fromisoformat(date_value)
    except ValueError as exc:
        raise PostError(
            f"invalid date {date_value!r} (expected YYYY-MM-DD)"
        ) from exc

    tags = _parse_tags(fields.get("tags", ""))

    return Post(slug=slug, title=title, date=date, body_markdown=body, tags=tags)


def load_post(path: Path) -> Post:
    """Load and parse a single post file. Errors mention the file name."""
    text = path.read_text(encoding="utf-8")
    try:
        return parse_post(text, slug=path.stem)
    except PostError as exc:
        raise PostError(f"{path.name}: {exc}") from exc


def load_posts(posts_dir: Path) -> list[Post]:
    """Load all posts from a directory, sorted newest first.

    Ties on the same date fall back to title order so the output is stable.
    """
    if not posts_dir.is_dir():
        raise PostError(f"posts directory not found: {posts_dir}")

    posts = [load_post(path) for path in sorted(posts_dir.glob("*.md"))]
    posts.sort(key=lambda post: (post.date, post.title), reverse=True)
    return posts
