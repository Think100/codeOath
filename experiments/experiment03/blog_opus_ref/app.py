# Simple Markdown Blog
# Run with: pip install flask markdown && python app.py
# Then open http://localhost:5000 in your browser.

import os
import glob
import datetime
import re

from flask import Flask, render_template, abort
import markdown

app = Flask(__name__)

POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts")


def parse_post(filepath):
    """Parse a markdown file with YAML-like front matter into a post dict."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Split front matter from body
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None

    front_matter = match.group(1)
    body_md = match.group(2)

    meta = {}
    for line in front_matter.strip().splitlines():
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if key and value:
            meta[key] = value

    title = meta.get("title", "Untitled")
    date_str = meta.get("date", "2000-01-01")
    tags_raw = meta.get("tags", "")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    try:
        date = datetime.date.fromisoformat(date_str)
    except ValueError:
        date = datetime.date(2000, 1, 1)

    slug = os.path.splitext(os.path.basename(filepath))[0]
    body_html = markdown.markdown(body_md, extensions=["fenced_code", "codehilite", "tables"])

    return {
        "title": title,
        "date": date,
        "tags": tags,
        "slug": slug,
        "body_html": body_html,
    }


def load_all_posts():
    """Load all posts from the posts directory, sorted newest first."""
    posts = []
    for filepath in glob.glob(os.path.join(POSTS_DIR, "*.md")):
        post = parse_post(filepath)
        if post:
            posts.append(post)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


@app.route("/")
def index():
    posts = load_all_posts()
    return render_template("index.html", posts=posts)


@app.route("/post/<slug>")
def post(slug):
    filepath = os.path.join(POSTS_DIR, f"{slug}.md")
    if not os.path.isfile(filepath):
        abort(404)
    post = parse_post(filepath)
    if not post:
        abort(404)
    return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
