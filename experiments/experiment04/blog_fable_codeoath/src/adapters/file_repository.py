"""Loads posts from a folder of Markdown files with YAML frontmatter.

Expected file format (posts/<slug>.md):

    ---
    title: My first post
    date: 2026-07-01
    tags: [python, web]        # optional
    ---
    Markdown body...
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import markdown
import yaml

from src.domain.models import Post, PostLoadError

FRONTMATTER_DELIMITER = "---"
MARKDOWN_EXTENSIONS = ["fenced_code", "tables"]


class PostFormatError(ValueError):
    """A post file that does not match the expected format."""


@dataclass(frozen=True)
class FileSystemPostRepository:
    """PostRepository implementation backed by a folder of .md files."""

    posts_dir: Path

    def load_all(self) -> tuple[list[Post], list[PostLoadError]]:
        """Parse every .md file. Broken files are reported, not fatal,
        so one bad post never hides the rest of the blog."""
        if not self.posts_dir.is_dir():
            # No posts folder is a setup problem, not a broken post: fail fast.
            raise FileNotFoundError(f"Posts folder not found: {self.posts_dir}")

        posts: list[Post] = []
        errors: list[PostLoadError] = []
        for path in sorted(self.posts_dir.glob("*.md")):
            try:
                posts.append(_parse_post_file(path))
            except (PostFormatError, OSError, yaml.YAMLError) as exc:
                errors.append(PostLoadError(source=path.name, reason=str(exc)))
        return posts, errors


def _parse_post_file(path: Path) -> Post:
    text = path.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(text)
    return Post(
        slug=path.stem,
        title=_require_title(meta),
        date=_require_date(meta),
        tags=_optional_tags(meta),
        html=markdown.markdown(body, extensions=MARKDOWN_EXTENSIONS),
    )


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """Split a post file into its YAML metadata dict and Markdown body."""
    if not text.startswith(FRONTMATTER_DELIMITER):
        raise PostFormatError("missing frontmatter block (file must start with ---)")
    try:
        _, meta_block, body = text.split(FRONTMATTER_DELIMITER, 2)
    except ValueError:
        raise PostFormatError("unclosed frontmatter block (second --- missing)") from None
    meta = yaml.safe_load(meta_block)
    if not isinstance(meta, dict):
        raise PostFormatError("frontmatter must be a YAML mapping (key: value lines)")
    return meta, body


def _require_title(meta: dict) -> str:
    title = meta.get("title")
    if not isinstance(title, str) or not title.strip():
        raise PostFormatError("frontmatter needs a non-empty 'title'")
    return title.strip()


def _require_date(meta: dict) -> date:
    value = meta.get("date")
    if isinstance(value, datetime):  # YAML parses timestamps as datetime
        return value.date()
    if isinstance(value, date):  # plain YYYY-MM-DD parses as date
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            raise PostFormatError(
                f"'date' must be an ISO date (YYYY-MM-DD), got: {value!r}"
            ) from None
    raise PostFormatError("frontmatter needs a 'date' (YYYY-MM-DD)")


def _optional_tags(meta: dict) -> tuple[str, ...]:
    value = meta.get("tags")
    if value is None:
        return ()
    if isinstance(value, str):  # allow "tags: python" shorthand
        return (value.strip(),)
    if isinstance(value, list) and all(isinstance(t, str) for t in value):
        return tuple(t.strip() for t in value if t.strip())
    raise PostFormatError("'tags' must be a list of strings, e.g. tags: [python, web]")
