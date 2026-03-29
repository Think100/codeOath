"""Ports (contracts) that infrastructure must implement.

These are the boundaries between domain and infrastructure.
The domain never imports infrastructure; infrastructure implements these protocols.
"""

from __future__ import annotations

from typing import List, Optional, Protocol

from src.domain.model import Post


class PostRepository(Protocol):
    """Contract for loading posts from storage."""

    def get_all(self) -> List[Post]:
        """Return all posts, newest first."""
        ...

    def get_by_slug(self, slug: str) -> Optional[Post]:
        """Return a single post by its slug, or None if not found."""
        ...


class MarkdownRenderer(Protocol):
    """Contract for converting Markdown to HTML."""

    def render(self, markdown_text: str) -> str:
        """Convert markdown source to an HTML fragment."""
        ...
