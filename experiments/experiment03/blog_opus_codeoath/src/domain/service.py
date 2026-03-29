"""Domain service: orchestrates reading posts and rendering them.

This is pure domain logic with no knowledge of Flask, files, or HTML templates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from src.domain.model import Post
from src.domain.ports import MarkdownRenderer, PostRepository


@dataclass
class BlogService:
    """Use-case layer for the blog."""

    repository: PostRepository
    renderer: MarkdownRenderer

    def list_posts(self) -> List[Post]:
        """Return all posts sorted newest-first."""
        posts = self.repository.get_all()
        return sorted(posts, key=lambda p: p.date, reverse=True)

    def get_post(self, slug: str) -> Optional[Tuple[Post, str]]:
        """Return a post and its rendered HTML, or None."""
        post = self.repository.get_by_slug(slug)
        if post is None:
            return None
        html = self.renderer.render(post.content_markdown)
        return post, html
