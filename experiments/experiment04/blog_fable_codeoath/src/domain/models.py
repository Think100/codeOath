"""Core blog concepts: what a post is and how posts are queried.

This module has no knowledge of files, YAML, Markdown, or Flask.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True, slots=True)
class Post:
    """A single blog post, fully parsed and ready to display."""

    slug: str  # URL identifier, derived from the source filename
    title: str
    date: date
    html: str  # post body, already rendered to HTML
    tags: tuple[str, ...] = field(default=())


@dataclass(frozen=True, slots=True)
class PostLoadError:
    """A post source that could not be loaded, with the reason why.

    Broken posts are skipped so the rest of the blog keeps working,
    but they must stay visible to the author (never swallowed).
    """

    source: str  # filename of the broken post
    reason: str


def sort_newest_first(posts: list[Post]) -> list[Post]:
    """Order posts by date, newest first. Ties break alphabetically by slug
    so the listing is deterministic."""
    return sorted(posts, key=lambda p: (-p.date.toordinal(), p.slug))


def filter_by_tag(posts: list[Post], tag: str) -> list[Post]:
    """All posts carrying the given tag (case-insensitive)."""
    wanted = tag.lower()
    return [p for p in posts if wanted in (t.lower() for t in p.tags)]


def find_by_slug(posts: list[Post], slug: str) -> Post | None:
    """The post with the given slug, or None if it does not exist."""
    return next((p for p in posts if p.slug == slug), None)
