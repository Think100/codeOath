# Simple Markdown blog. To run:
#
#   pip install flask markdown pyyaml
#   python app.py
#
# Then open http://localhost:5000 in your browser.
# Posts live in the posts/ directory as Markdown files with YAML front matter.

from pathlib import Path

from flask import Flask

from src.infrastructure.file_repository import FilePostRepository
from src.web.routes import bp

POSTS_DIR = Path(__file__).parent / "posts"


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="src/web/templates",
    )

    repo = FilePostRepository(POSTS_DIR)
    app.config["POST_REPOSITORY"] = repo

    app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found(error):
        return "<h1>404 - Post not found</h1><p><a href='/'>Back to index</a></p>", 404

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(debug=True, port=5000)
