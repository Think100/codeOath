# Simple Markdown Blog
#
# How to run:
#   1. Install dependencies: pip install flask markdown python-frontmatter
#   2. Run: python app.py
#   3. Open http://localhost:5000 in your browser
#
# Posts are Markdown files in the ./posts/ directory.
# Each post must have front matter with: title, date, and optionally tags.

from pathlib import Path
from datetime import date

import frontmatter
import markdown
from flask import Flask, render_template, abort

app = Flask(__name__)

POSTS_DIR = Path(__file__).parent / "posts"


def load_post(filepath: Path) -> dict:
    """Load a single post from a Markdown file with front matter."""
    post = frontmatter.load(filepath)
    slug = filepath.stem
    raw_date = post.metadata.get("date", date.min)
    # frontmatter may return a date object or a string
    if isinstance(raw_date, str):
        raw_date = date.fromisoformat(raw_date)
    return {
        "slug": slug,
        "title": post.metadata.get("title", slug),
        "date": raw_date,
        "tags": post.metadata.get("tags", []),
        "content_md": post.content,
        "content_html": markdown.markdown(post.content, extensions=["fenced_code", "codehilite"]),
    }


def load_all_posts() -> list[dict]:
    """Load all posts, sorted newest first."""
    posts = [load_post(f) for f in POSTS_DIR.glob("*.md")]
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


@app.route("/")
def index():
    posts = load_all_posts()
    return render_template("index.html", posts=posts)


@app.route("/post/<slug>")
def post(slug: str):
    filepath = POSTS_DIR / f"{slug}.md"
    if not filepath.exists():
        abort(404)
    p = load_post(filepath)
    return render_template("post.html", post=p)


if __name__ == "__main__":
    app.run(debug=True)
