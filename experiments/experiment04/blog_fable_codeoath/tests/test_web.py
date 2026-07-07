from datetime import date

import pytest

from src.adapters.web import create_app
from src.domain.models import Post, PostLoadError


class FakeRepository:
    """In-memory PostRepository (matches the Protocol structurally)."""

    def __init__(self, posts=(), errors=()):
        self.posts = list(posts)
        self.errors = list(errors)

    def load_all(self):
        return self.posts, self.errors


def make_post(slug: str, on: str, tags=()) -> Post:
    return Post(
        slug=slug,
        title=f"Title of {slug}",
        date=date.fromisoformat(on),
        html=f"<p>Body of {slug}</p>",
        tags=tuple(tags),
    )


@pytest.fixture
def client():
    posts = [
        make_post("older", "2026-06-01", tags=["python"]),
        make_post("newest", "2026-07-04", tags=["python", "web"]),
    ]
    errors = [PostLoadError(source="broken.md", reason="frontmatter needs a 'date'")]
    app = create_app(FakeRepository(posts, errors))
    app.config["TESTING"] = True
    return app.test_client()


def test_index_lists_posts_newest_first(client):
    html = client.get("/").text
    assert html.index("Title of newest") < html.index("Title of older")


def test_index_shows_load_errors(client):
    html = client.get("/").text
    assert "broken.md" in html
    assert "frontmatter needs a" in html


def test_post_page_renders_body(client):
    response = client.get("/posts/older")
    assert response.status_code == 200
    assert "<p>Body of older</p>" in response.text


def test_unknown_post_returns_404(client):
    assert client.get("/posts/ghost").status_code == 404


def test_tag_page_filters_posts(client):
    html = client.get("/tags/web").text
    assert "Title of newest" in html
    assert "Title of older" not in html


def test_unknown_tag_returns_404(client):
    assert client.get("/tags/gardening").status_code == 404
