"""Tests for domain model and service logic."""

import os
import sys
from datetime import date

# Ensure project root is on path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.domain.model import Post
from src.domain.service import BlogService


# --- Fake adapters for testing (no filesystem, no real markdown lib) ---

class FakeRepository:
    def __init__(self, posts):
        self._posts = posts

    def get_all(self):
        return list(self._posts)

    def get_by_slug(self, slug):
        for p in self._posts:
            if p.slug == slug:
                return p
        return None


class FakeRenderer:
    def render(self, markdown_text):
        return f"<p>{markdown_text}</p>"


# --- Tests ---

def test_post_creation():
    post = Post(slug="test", title="Test", date=date(2025, 1, 1), content_markdown="hello")
    assert post.title == "Test"
    assert post.tags == []


def test_post_requires_slug():
    try:
        Post(slug="", title="Test", date=date(2025, 1, 1), content_markdown="x")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_post_requires_title():
    try:
        Post(slug="test", title="", date=date(2025, 1, 1), content_markdown="x")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_service_list_posts_sorted():
    posts = [
        Post(slug="old", title="Old", date=date(2024, 1, 1), content_markdown="a"),
        Post(slug="new", title="New", date=date(2025, 6, 1), content_markdown="b"),
        Post(slug="mid", title="Mid", date=date(2024, 6, 1), content_markdown="c"),
    ]
    service = BlogService(repository=FakeRepository(posts), renderer=FakeRenderer())
    result = service.list_posts()
    assert [p.slug for p in result] == ["new", "mid", "old"]


def test_service_get_post():
    posts = [Post(slug="hello", title="Hello", date=date(2025, 1, 1), content_markdown="world")]
    service = BlogService(repository=FakeRepository(posts), renderer=FakeRenderer())
    result = service.get_post("hello")
    assert result is not None
    post, html = result
    assert post.slug == "hello"
    assert "<p>world</p>" in html


def test_service_get_post_not_found():
    service = BlogService(repository=FakeRepository([]), renderer=FakeRenderer())
    assert service.get_post("nonexistent") is None


if __name__ == "__main__":
    test_post_creation()
    test_post_requires_slug()
    test_post_requires_title()
    test_service_list_posts_sorted()
    test_service_get_post()
    test_service_get_post_not_found()
    print("All tests passed.")
