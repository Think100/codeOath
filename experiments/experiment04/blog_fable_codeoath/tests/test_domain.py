from datetime import date

from src.domain.models import Post, filter_by_tag, find_by_slug, sort_newest_first


def make_post(slug: str, on: str, tags: tuple[str, ...] = ()) -> Post:
    return Post(slug=slug, title=slug, date=date.fromisoformat(on), html="", tags=tags)


def test_sort_newest_first():
    posts = [
        make_post("old", "2026-01-01"),
        make_post("new", "2026-07-04"),
        make_post("mid", "2026-03-15"),
    ]
    assert [p.slug for p in sort_newest_first(posts)] == ["new", "mid", "old"]


def test_sort_breaks_date_ties_by_slug():
    posts = [make_post("beta", "2026-07-01"), make_post("alpha", "2026-07-01")]
    assert [p.slug for p in sort_newest_first(posts)] == ["alpha", "beta"]


def test_filter_by_tag_is_case_insensitive():
    posts = [
        make_post("a", "2026-01-01", tags=("Python", "web")),
        make_post("b", "2026-01-02", tags=("rust",)),
        make_post("c", "2026-01-03"),  # untagged
    ]
    assert [p.slug for p in filter_by_tag(posts, "python")] == ["a"]
    assert filter_by_tag(posts, "missing") == []


def test_find_by_slug():
    posts = [make_post("a", "2026-01-01"), make_post("b", "2026-01-02")]
    assert find_by_slug(posts, "b").slug == "b"
    assert find_by_slug(posts, "nope") is None
