"""Outgoing adapter: implements ``PostRepository`` by reading Markdown files
with YAML frontmatter from disk.

This is where all the infrastructure concerns live: file I/O, YAML parsing,
Markdown rendering, and logging. The domain never sees any of this.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from pathlib import Path

import frontmatter
import markdown as markdown_lib
import yaml

from blog.domain.models import Post, PostValidationError, sort_newest_first

logger = logging.getLogger(__name__)

# Fenced code blocks and tables cover most technical blog writing without
# pulling in a large extension set.
_MARKDOWN_EXTENSIONS = ["fenced_code", "tables"]


class FileSystemPostRepository:
    """Implements ``PostRepository`` by reading ``*.md`` files from a folder.

    Each file's name (without extension) becomes the post's slug and its
    URL. A post that cannot be parsed is skipped: a warning is logged with
    the filename and reason, and the rest of the blog keeps working. One
    broken file should never take down the whole site.
    """

    def __init__(self, posts_dir: Path) -> None:
        self._posts_dir = posts_dir

    def list_posts(self) -> list[Post]:
        posts = []
        for path in sorted(self._posts_dir.glob("*.md")):
            post = self._load(path)
            if post is not None:
                posts.append(post)
        return sort_newest_first(posts)

    def get_post(self, slug: str) -> Post | None:
        path = self._posts_dir / f"{slug}.md"
        if not path.exists():
            return None
        return self._load(path)

    def _load(self, path: Path) -> Post | None:
        try:
            with path.open("r", encoding="utf-8") as handle:
                parsed = frontmatter.load(handle)
        except OSError as exc:
            logger.warning("could not read post file %s: %s", path.name, exc)
            return None
        except yaml.YAMLError as exc:
            logger.warning("could not parse frontmatter in %s: %s", path.name, exc)
            return None

        try:
            return self._to_post(path, parsed)
        except PostValidationError as exc:
            logger.warning("skipping invalid post %s: %s", path.name, exc)
            return None

    def _to_post(self, path: Path, parsed: frontmatter.Post) -> Post:
        title = parsed.get("title")
        published_raw = parsed.get("date")
        if not title or published_raw is None:
            raise PostValidationError(
                f"'{path.name}' is missing a required 'title' or 'date' field"
            )

        published = _parse_date(published_raw, path.name)
        tags = tuple(str(tag) for tag in (parsed.get("tags") or ()))
        content_html = markdown_lib.markdown(parsed.content, extensions=_MARKDOWN_EXTENSIONS)

        return Post(
            slug=path.stem,
            title=str(title),
            published=published,
            tags=tags,
            content_html=content_html,
        )


def _parse_date(value: object, filename: str) -> date:
    """Frontmatter dates come back as ``date`` objects when written as bare
    YAML dates (``date: 2026-06-01``) and as ``str`` when quoted. Accept
    both, reject anything else with a domain error."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as exc:
            raise PostValidationError(
                f"'{filename}' has an invalid date '{value}' (expected YYYY-MM-DD)"
            ) from exc
    raise PostValidationError(f"'{filename}' has an invalid 'date' value: {value!r}")
