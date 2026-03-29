"""Infrastructure adapter: Flask web layer.

Handles HTTP routing and HTML template rendering.
All domain logic is delegated to BlogService.
"""

from __future__ import annotations

import os

from flask import Flask, abort, render_template

from src.domain.service import BlogService

# Project root is three levels up from this file (src/infrastructure/web.py)
_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


def create_app(blog_service: BlogService) -> Flask:
    """Build and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder=os.path.join(_PROJECT_ROOT, "templates"),
        static_folder=os.path.join(_PROJECT_ROOT, "static"),
    )

    @app.route("/")
    def index():
        posts = blog_service.list_posts()
        return render_template("index.html", posts=posts)

    @app.route("/post/<slug>")
    def post_detail(slug: str):
        result = blog_service.get_post(slug)
        if result is None:
            abort(404)
        post, html_content = result
        return render_template("post.html", post=post, content=html_content)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app
