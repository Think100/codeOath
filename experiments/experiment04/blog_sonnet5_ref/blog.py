"""Core logic for loading Markdown blog posts and their metadata.

Posts live as .md files in the posts/ directory. Each file starts with a
simple frontmatter block (delimited by "---" lines) that holds the title,
date, and optional tags, followed by the Markdown body.

Example post file:

    ---
    title: Hello World
    date: 2026-01-01
    tags: intro, meta
    ---

    This is the post body, written in **Markdown**.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import date, datetime

import markdown

POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts")

# Matches a leading "---\n ... \n---\n" frontmatter block, capturing the
# metadata lines and the remaining body text separately.
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?\n)---\s*\n(.*)$", re.DOTALL)


@dataclass
class Post:
    slug: str
    title: str
    date: date
    tags: list[str]
    html: str

    @property
    def display_date(self) -> str:
        return self.date.strftime("%B %d, %Y")


def _parse_frontmatter(raw_text: str) -> tuple[dict[str, str], str]:
    """Split a post file's raw text into its metadata dict and Markdown body."""
    match = FRONTMATTER_PATTERN.match(raw_text)
    if not match:
        raise ValueError("missing '---' frontmatter block at the top of the file")

    frontmatter_block, body = match.groups()

    metadata: dict[str, str] = {}
    for line in frontmatter_block.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip()

    return metadata, body.strip()


def _load_post_from_file(file_path: str) -> Post:
    slug = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    metadata, body = _parse_frontmatter(raw_text)

    title = metadata.get("title", slug)

    date_str = metadata.get("date")
    if not date_str:
        raise ValueError("missing required 'date' field")
    try:
        post_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"'date' must be in YYYY-MM-DD format, got '{date_str}'") from exc

    tags_str = metadata.get("tags", "")
    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

    html = markdown.markdown(body, extensions=["fenced_code", "tables"])

    return Post(slug=slug, title=title, date=post_date, tags=tags, html=html)


def load_all_posts() -> list[Post]:
    """Load every post from the posts directory, sorted newest first.

    Posts with invalid or missing frontmatter are skipped, with a warning
    printed to the console, rather than crashing the whole site.
    """
    posts: list[Post] = []
    if not os.path.isdir(POSTS_DIR):
        return posts

    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith(".md"):
            continue
        file_path = os.path.join(POSTS_DIR, filename)
        try:
            posts.append(_load_post_from_file(file_path))
        except ValueError as exc:
            print(f"Skipping post '{filename}': {exc}")

    posts.sort(key=lambda p: p.date, reverse=True)
    return posts


def load_post_by_slug(slug: str) -> Post | None:
    """Load a single post by its slug (filename without .md), or None if missing/invalid."""
    file_path = os.path.join(POSTS_DIR, f"{slug}.md")
    if not os.path.isfile(file_path):
        return None
    try:
        return _load_post_from_file(file_path)
    except ValueError as exc:
        print(f"Cannot load post '{slug}': {exc}")
        return None
