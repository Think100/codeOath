from flask import Blueprint, abort, render_template

from src.domain.ports import PostRepository

bp = Blueprint("blog", __name__)

# Repository is injected via app config after blueprint registration.
# Access it through current_app to avoid circular imports.
from flask import current_app


def _repo() -> PostRepository:
    return current_app.config["POST_REPOSITORY"]


@bp.route("/")
def index():
    posts = _repo().get_all()
    return render_template("index.html", posts=posts)


@bp.route("/post/<slug>")
def post_detail(slug: str):
    post = _repo().get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("post.html", post=post)
