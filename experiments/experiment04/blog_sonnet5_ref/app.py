"""Flask web app that serves the Markdown blog.

Run with:  python app.py
Then open: http://127.0.0.1:5000
"""

from flask import Flask, abort, render_template

from blog import load_all_posts, load_post_by_slug

app = Flask(__name__)


@app.route("/")
def index():
    """Main page: all posts, newest first."""
    posts = load_all_posts()
    return render_template("index.html", posts=posts)


@app.route("/post/<slug>")
def post(slug):
    """Individual post page, looked up by its URL slug."""
    found_post = load_post_by_slug(slug)
    if found_post is None:
        abort(404)
    return render_template("post.html", post=found_post)


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
