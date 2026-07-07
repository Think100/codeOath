"""Ports: what the web layer needs from a post storage, without knowing how
posts are actually stored.

An adapter (e.g. ``blog.adapters.markdown_repository.FileSystemPostRepository``)
implements this contract. Thanks to Python's structural typing, an adapter
does not need to inherit from ``PostRepository``; matching method signatures
is enough.
"""

from __future__ import annotations

from typing import Protocol

from blog.domain.models import Post


class PostRepository(Protocol):
    """Read access to blog posts, newest first."""

    def list_posts(self) -> list[Post]:
        """Return all valid posts, newest first. Malformed posts are left out
        by the adapter; this port never sees them."""
        ...

    def get_post(self, slug: str) -> Post | None:
        """Return a single post by slug, or ``None`` if it does not exist
        (or could not be parsed)."""
        ...
