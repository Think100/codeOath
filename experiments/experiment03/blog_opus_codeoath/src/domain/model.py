"""Domain model for the blog system.

A Post is the core entity: title, date, tags, and markdown content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass(frozen=True)
class Post:
    """A single blog post."""

    slug: str
    title: str
    date: date
    content_markdown: str
    tags: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.slug:
            raise ValueError("Post slug must not be empty")
        if not self.title:
            raise ValueError("Post title must not be empty")
