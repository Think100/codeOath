"""Adapter tests: real files on disk, via pytest's tmp_path fixture."""

from datetime import date
from pathlib import Path

from blog.adapters.markdown_repository import FileSystemPostRepository


def _write(posts_dir: Path, filename: str, content: str) -> None:
    (posts_dir / filename).write_text(content, encoding="utf-8")


def test_list_posts_parses_valid_posts_newest_first(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "first.md",
        "---\ntitle: First Post\ndate: 2026-01-01\ntags: [intro]\n---\n\nHello.\n",
    )
    _write(
        tmp_path,
        "second.md",
        "---\ntitle: Second Post\ndate: 2026-06-01\n---\n\nWorld.\n",
    )

    repository = FileSystemPostRepository(tmp_path)
    posts = repository.list_posts()

    assert [post.slug for post in posts] == ["second", "first"]
    assert posts[1].tags == ("intro",)
    assert posts[0].published == date(2026, 6, 1)
    assert "<p>World.</p>" in posts[0].content_html


def test_list_posts_skips_malformed_posts(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "good.md",
        "---\ntitle: Good Post\ndate: 2026-01-01\n---\n\nFine.\n",
    )
    # Missing the required 'date' field.
    _write(
        tmp_path,
        "missing-date.md",
        "---\ntitle: No Date Here\n---\n\nBroken.\n",
    )
    # Invalid YAML in the frontmatter block.
    _write(
        tmp_path,
        "bad-yaml.md",
        "---\ntitle: [unterminated\ndate: 2026-01-01\n---\n\nBroken.\n",
    )

    repository = FileSystemPostRepository(tmp_path)
    posts = repository.list_posts()

    assert [post.slug for post in posts] == ["good"]


def test_get_post_returns_none_for_unknown_slug(tmp_path: Path) -> None:
    repository = FileSystemPostRepository(tmp_path)
    assert repository.get_post("does-not-exist") is None


def test_get_post_returns_none_for_malformed_post(tmp_path: Path) -> None:
    _write(tmp_path, "broken.md", "---\ntitle: Broken\n---\n\nNo date.\n")

    repository = FileSystemPostRepository(tmp_path)

    assert repository.get_post("broken") is None
