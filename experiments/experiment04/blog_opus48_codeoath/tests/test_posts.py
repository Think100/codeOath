"""Tests for post parsing and loading."""

import datetime as dt

import pytest

from blog.posts import PostError, load_posts, parse_post

VALID = """\
---
title: Hello World
date: 2026-06-01
tags: intro, meta
---

Body **here**.
"""


def test_parse_valid_post():
    post = parse_post(VALID, slug="hello")
    assert post.slug == "hello"
    assert post.title == "Hello World"
    assert post.date == dt.date(2026, 6, 1)
    assert post.tags == ["intro", "meta"]
    assert "<strong>here</strong>" in post.html


def test_tags_are_optional():
    text = "---\ntitle: T\ndate: 2026-01-01\n---\nbody"
    assert parse_post(text, slug="t").tags == []


def test_missing_front_matter_raises():
    with pytest.raises(PostError):
        parse_post("no front matter", slug="x")


def test_unclosed_front_matter_raises():
    with pytest.raises(PostError):
        parse_post("---\ntitle: T\ndate: 2026-01-01\n", slug="x")


def test_missing_title_raises():
    with pytest.raises(PostError):
        parse_post("---\ndate: 2026-01-01\n---\nbody", slug="x")


def test_missing_date_raises():
    with pytest.raises(PostError):
        parse_post("---\ntitle: T\n---\nbody", slug="x")


def test_invalid_date_raises():
    with pytest.raises(PostError):
        parse_post("---\ntitle: T\ndate: 01-06-2026\n---\nbody", slug="x")


def test_date_display_format():
    post = parse_post(VALID, slug="hello")
    assert post.date_display == "01 June 2026"


def test_load_posts_sorted_newest_first(tmp_path):
    (tmp_path / "old.md").write_text(
        "---\ntitle: Old\ndate: 2026-01-01\n---\nold", encoding="utf-8"
    )
    (tmp_path / "new.md").write_text(
        "---\ntitle: New\ndate: 2026-12-31\n---\nnew", encoding="utf-8"
    )
    posts = load_posts(tmp_path)
    assert [p.title for p in posts] == ["New", "Old"]


def test_load_posts_missing_dir_raises(tmp_path):
    with pytest.raises(PostError):
        load_posts(tmp_path / "does-not-exist")


def test_load_post_error_mentions_filename(tmp_path):
    (tmp_path / "broken.md").write_text("no front matter", encoding="utf-8")
    with pytest.raises(PostError, match="broken.md"):
        load_posts(tmp_path)
