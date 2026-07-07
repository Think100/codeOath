from datetime import date

import pytest

from src.adapters.file_repository import FileSystemPostRepository

VALID_POST = """---
title: A valid post
date: 2026-07-01
tags: [python, web]
---
Body with **bold** text.
"""


def write(tmp_path, name: str, content: str) -> None:
    (tmp_path / name).write_text(content, encoding="utf-8")


def load(tmp_path):
    return FileSystemPostRepository(posts_dir=tmp_path).load_all()


def test_parses_valid_post(tmp_path):
    write(tmp_path, "valid.md", VALID_POST)
    posts, errors = load(tmp_path)
    assert errors == []
    (post,) = posts
    assert post.slug == "valid"
    assert post.title == "A valid post"
    assert post.date == date(2026, 7, 1)
    assert post.tags == ("python", "web")
    assert "<strong>bold</strong>" in post.html


def test_tags_are_optional(tmp_path):
    write(tmp_path, "untagged.md", "---\ntitle: T\ndate: 2026-01-01\n---\nHi\n")
    posts, errors = load(tmp_path)
    assert errors == []
    assert posts[0].tags == ()


def test_broken_post_is_reported_but_others_still_load(tmp_path):
    write(tmp_path, "valid.md", VALID_POST)
    write(tmp_path, "no-title.md", "---\ndate: 2026-01-01\n---\nBody\n")
    posts, errors = load(tmp_path)
    assert [p.slug for p in posts] == ["valid"]
    (error,) = errors
    assert error.source == "no-title.md"
    assert "title" in error.reason


@pytest.mark.parametrize(
    ("content", "reason_fragment"),
    [
        ("No frontmatter at all\n", "missing frontmatter"),
        ("---\ntitle: T\ndate: 2026-01-01\nBody without closing\n", "unclosed"),
        ("---\ntitle: T\n---\nBody\n", "date"),
        ("---\ntitle: T\ndate: not-a-date\n---\nBody\n", "ISO date"),
        ("---\ntitle: T\ndate: 2026-01-01\ntags: {a: b}\n---\nBody\n", "tags"),
    ],
)
def test_malformed_posts_produce_clear_errors(tmp_path, content, reason_fragment):
    write(tmp_path, "bad.md", content)
    posts, errors = load(tmp_path)
    assert posts == []
    assert reason_fragment in errors[0].reason


def test_missing_posts_folder_fails_fast(tmp_path):
    repo = FileSystemPostRepository(posts_dir=tmp_path / "does-not-exist")
    with pytest.raises(FileNotFoundError):
        repo.load_all()
