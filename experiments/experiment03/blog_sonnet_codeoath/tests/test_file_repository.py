import tempfile
from datetime import date
from pathlib import Path

import pytest

from src.infrastructure.file_repository import FilePostRepository


def make_post_file(directory: Path, slug: str, content: str) -> None:
    (directory / f"{slug}.md").write_text(content, encoding="utf-8")


VALID_POST = """\
---
title: Test Post
date: 2024-06-01
tags: [test, example]
---

This is the **body**.
"""

MISSING_TITLE = """\
---
date: 2024-06-01
---

Body here.
"""

NO_FRONT_MATTER = "Just plain text, no front matter."


def test_loads_valid_post():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        make_post_file(d, "test-post", VALID_POST)
        repo = FilePostRepository(d)
        posts = repo.get_all()

        assert len(posts) == 1
        p = posts[0]
        assert p.slug == "test-post"
        assert p.title == "Test Post"
        assert p.date == date(2024, 6, 1)
        assert "test" in p.tags
        assert "<strong>body</strong>" in p.content_html


def test_sorted_newest_first():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        make_post_file(d, "old-post", VALID_POST.replace("2024-06-01", "2023-01-01"))
        make_post_file(d, "new-post", VALID_POST.replace("2024-06-01", "2025-12-31"))
        repo = FilePostRepository(d)
        posts = repo.get_all()

        assert posts[0].slug == "new-post"
        assert posts[1].slug == "old-post"


def test_get_by_slug_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        make_post_file(d, "test-post", VALID_POST)
        repo = FilePostRepository(d)

        post = repo.get_by_slug("test-post")
        assert post is not None
        assert post.slug == "test-post"


def test_get_by_slug_not_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        make_post_file(d, "test-post", VALID_POST)
        repo = FilePostRepository(d)

        assert repo.get_by_slug("does-not-exist") is None


def test_missing_title_raises():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        make_post_file(d, "bad-post", MISSING_TITLE)
        repo = FilePostRepository(d)

        with pytest.raises(RuntimeError, match="title"):
            repo.get_all()


def test_no_front_matter_raises():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        make_post_file(d, "bad-post", NO_FRONT_MATTER)
        repo = FilePostRepository(d)

        with pytest.raises(RuntimeError, match="front matter"):
            repo.get_all()


def test_empty_directory_returns_empty_list():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = FilePostRepository(Path(tmpdir))
        assert repo.get_all() == []
