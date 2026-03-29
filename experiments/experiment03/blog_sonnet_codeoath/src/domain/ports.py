from typing import Protocol

from .model import Post


class PostRepository(Protocol):
    """Contract for loading blog posts. Infrastructure must implement this."""

    def get_all(self) -> list[Post]:
        """Return all posts, sorted newest first."""
        ...

    def get_by_slug(self, slug: str) -> Post | None:
        """Return a single post by its slug, or None if not found."""
        ...
