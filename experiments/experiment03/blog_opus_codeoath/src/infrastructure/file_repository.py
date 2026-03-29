"""Infrastructure adapter: loads posts from Markdown files on disk.

Each .md file in the posts/ directory is one post.
The file must start with a YAML-like front-matter block delimited by '---':

    ---
    title: My Post Title
    date: 2025-01-15
    tags: python, web
    ---

    Markdown body here...

The filename (without .md) becomes the post slug.
"""

from __future__ import annotations

import os
import re
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional

from src.domain.model import Post


class FilePostRepository:
    """Implements PostRepository port by reading .md files from a directory."""

    def __init__(self, posts_dir: str) -> None:
        self._posts_dir = Path(posts_dir)
        if not self._posts_dir.is_dir():
            raise FileNotFoundError(f"Posts directory not found: {posts_dir}")

    def get_all(self) -> List[Post]:
        posts: List[Post] = []
        for filepath in sorted(self._posts_dir.glob("*.md")):
            post = self._load(filepath)
            if post is not None:
                posts.append(post)
        return sorted(posts, key=lambda p: p.date, reverse=True)

    def get_by_slug(self, slug: str) -> Optional[Post]:
        filepath = self._posts_dir / f"{slug}.md"
        if not filepath.is_file():
            return None
        return self._load(filepath)

    # --- internal helpers ---

    _FRONT_MATTER_RE = re.compile(
        r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL
    )

    def _load(self, filepath: Path) -> Optional[Post]:
        text = filepath.read_text(encoding="utf-8")
        match = self._FRONT_MATTER_RE.match(text)
        if not match:
            return None  # skip files without valid front-matter

        meta_block, body = match.group(1), match.group(2)
        meta = self._parse_front_matter(meta_block)

        title = meta.get("title", "")
        if not title:
            return None

        date_str = meta.get("date", "")
        try:
            post_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            post_date = date.today()

        tags_raw = meta.get("tags", "")
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

        slug = filepath.stem
        return Post(
            slug=slug,
            title=title,
            date=post_date,
            content_markdown=body.strip(),
            tags=tags,
        )

    @staticmethod
    def _parse_front_matter(block: str) -> Dict[str, str]:
        result: Dict[str, str] = {}
        for line in block.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                result[key.strip().lower()] = value.strip()
        return result
