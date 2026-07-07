"""Flask routes: turns domain data into HTML pages."""

from __future__ import annotations

from datetime import date

from flask import Flask, abort, render_template

from src.domain.models import filter_by_tag, find_by_slug, sort_newest_first
from src.domain.ports import PostRepository


def create_app(repository: PostRepository) -> Flask:
    app = Flask(__name__)

    @app.template_filter("humandate")
    def humandate(value: date) -> str:
        return f"{value.day} {value.strftime('%B %Y')}"

    def load_posts():
        # Posts are re-read per request so edits to .md files show up on
        # refresh. Fine for a local blog with a handful of files.
        posts, errors = repository.load_all()
        return sort_newest_first(posts), errors

    @app.route("/")
    def index():
        posts, errors = load_posts()
        return render_template("index.html", posts=posts, errors=errors, tag=None)

    @app.route("/posts/<slug>")
    def post_detail(slug: str):
        posts, _ = load_posts()
        post = find_by_slug(posts, slug)
        if post is None:
            abort(404)
        return render_template("post.html", post=post)

    @app.route("/tags/<tag>")
    def posts_by_tag(tag: str):
        posts, errors = load_posts()
        tagged = filter_by_tag(posts, tag)
        if not tagged:
            abort(404)
        return render_template("index.html", posts=tagged, errors=errors, tag=tag)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("not_found.html"), 404

    return app
