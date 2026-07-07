"""Incoming adapter: translates HTTP requests into calls against a
``PostRepository`` port and renders the results as HTML.

This module never reads files directly and never imports the concrete
``FileSystemPostRepository``; it only depends on the ``PostRepository``
port. ``main.py`` decides which adapter actually fulfills that port.
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, abort, render_template

from blog.domain.ports import PostRepository


def create_app(repository: PostRepository, template_folder: Path, static_folder: Path) -> Flask:
    """Build the Flask app and wire its routes to the given repository."""
    app = Flask(
        __name__,
        template_folder=str(template_folder),
        static_folder=str(static_folder),
    )

    @app.route("/")
    def index():
        return render_template("index.html", posts=repository.list_posts())

    @app.route("/posts/<slug>")
    def show_post(slug: str):
        post = repository.get_post(slug)
        if post is None:
            abort(404)
        return render_template("post.html", post=post)

    @app.errorhandler(404)
    def not_found(_error: object):
        return render_template("404.html"), 404

    return app
