"""Domain model for blog posts.

No external dependencies here (no Flask, no Markdown parser, no filesystem).
This module only knows what a post *is* and the one business rule attached
to it: newest posts come first.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


class PostValidationError(ValueError):
    """Raised when a post's metadata does not meet the domain's requirements.

    This is a domain-level error, not a parsing error. Adapters translate
    file-format problems (bad YAML, unreadable files) into this error so the
    web layer only ever has to deal with one kind of "this post is broken".
    """


@dataclass(frozen=True, slots=True)
class Post:
    """A single blog post, already parsed and rendered.

    ``content_html`` holds the rendered HTML body. Markdown rendering is an
    infrastructure concern (it depends on a third-party library), so the
    adapter does the rendering and hands the domain a finished string.
    """

    slug: str
    title: str
    published: date
    tags: tuple[str, ...] = field(default_factory=tuple)
    content_html: str = ""

    def __post_init__(self) -> None:
        if not self.slug:
            raise PostValidationError("post is missing a slug")
        if not self.title.strip():
            raise PostValidationError(f"post '{self.slug}' is missing a title")


def sort_newest_first(posts: list[Post]) -> list[Post]:
    """Business rule: the blog always shows the most recent post first."""
    return sorted(posts, key=lambda post: post.published, reverse=True)
