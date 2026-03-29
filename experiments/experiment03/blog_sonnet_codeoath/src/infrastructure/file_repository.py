import re
from datetime import date
from pathlib import Path

import markdown
import yaml

from src.domain.model import Post


def _parse_front_matter(text: str) -> tuple[dict, str]:
    """
    Split YAML front matter from Markdown body.
    Front matter must be wrapped in --- lines at the top of the file.
    Raises ValueError if front matter is missing or malformed.
    """
    pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)", re.DOTALL)
    match = pattern.match(text)
    if not match:
        raise ValueError("Post file is missing YAML front matter (--- ... ---)")

    raw_yaml, body = match.group(1), match.group(2)
    try:
        meta = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in front matter: {exc}") from exc

    if not isinstance(meta, dict):
        raise ValueError("Front matter must be a YAML mapping")

    return meta, body


def _build_post(slug: str, meta: dict, body: str) -> Post:
    """Validate metadata and construct a Post. Fails fast on missing fields."""
    title = meta.get("title")
    if not title:
        raise ValueError(f"Post '{slug}' is missing required field: title")

    raw_date = meta.get("date")
    if not raw_date:
        raise ValueError(f"Post '{slug}' is missing required field: date")

    if isinstance(raw_date, date):
        post_date = raw_date
    else:
        try:
            post_date = date.fromisoformat(str(raw_date))
        except ValueError as exc:
            raise ValueError(f"Post '{slug}': invalid date '{raw_date}'") from exc

    tags = meta.get("tags") or []
    if not isinstance(tags, list):
        tags = [str(tags)]

    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
    content_html = md.convert(body)

    return Post(
        slug=slug,
        title=str(title),
        date=post_date,
        tags=[str(t) for t in tags],
        content_md=body,
        content_html=content_html,
    )


class FilePostRepository:
    """
    Loads posts from Markdown files in a directory.
    Each file: <slug>.md with YAML front matter.
    Implements PostRepository protocol.
    """

    def __init__(self, posts_dir: Path) -> None:
        if not posts_dir.exists():
            raise FileNotFoundError(f"Posts directory not found: {posts_dir}")
        self._posts_dir = posts_dir
        self._cache: list[Post] | None = None

    def _load_all(self) -> list[Post]:
        posts = []
        for path in self._posts_dir.glob("*.md"):
            slug = path.stem
            try:
                text = path.read_text(encoding="utf-8")
                meta, body = _parse_front_matter(text)
                post = _build_post(slug, meta, body)
                posts.append(post)
            except (ValueError, OSError) as exc:
                # Fail fast: a broken post file is a bug, not a recoverable state.
                raise RuntimeError(f"Failed to load post '{path.name}': {exc}") from exc
        return sorted(posts, key=lambda p: p.date, reverse=True)

    def get_all(self) -> list[Post]:
        if self._cache is None:
            self._cache = self._load_all()
        return self._cache

    def get_by_slug(self, slug: str) -> Post | None:
        return next((p for p in self.get_all() if p.slug == slug), None)
