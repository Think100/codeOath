"""Domain tests: pure logic, no filesystem, no Flask."""

from datetime import date

import pytest

from blog.domain.models import Post, PostValidationError, sort_newest_first


def test_post_requires_a_title() -> None:
    with pytest.raises(PostValidationError):
        Post(slug="empty-title", title="   ", published=date(2026, 1, 1))


def test_post_requires_a_slug() -> None:
    with pytest.raises(PostValidationError):
        Post(slug="", title="Untitled", published=date(2026, 1, 1))


def test_sort_newest_first_orders_by_published_date() -> None:
    oldest = Post(slug="oldest", title="Oldest", published=date(2026, 1, 1))
    newest = Post(slug="newest", title="Newest", published=date(2026, 6, 1))
    middle = Post(slug="middle", title="Middle", published=date(2026, 3, 1))

    result = sort_newest_first([oldest, newest, middle])

    assert [post.slug for post in result] == ["newest", "middle", "oldest"]


def test_post_tags_default_to_empty_tuple() -> None:
    post = Post(slug="no-tags", title="No Tags", published=date(2026, 1, 1))
    assert post.tags == ()
