"""Local web server for the blog, built on the standard library.

Routes:
  GET /                 -> index page, all posts newest first
  GET /post/<slug>      -> a single post
  GET /static/style.css -> the stylesheet

Posts are reloaded from disk on every request so editing a .md file and
refreshing the browser is enough to see changes; no restart needed.
"""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from . import render
from .posts import PostError, load_posts

# Project root is two levels up from this file: src/blog/app.py -> project/
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POSTS_DIR = _PROJECT_ROOT / "posts"


class BlogHandler(BaseHTTPRequestHandler):
    """Serves blog pages. ``posts_dir`` is injected by the server factory."""

    posts_dir: Path = DEFAULT_POSTS_DIR
    server_version = "markblog/1.0"

    def do_GET(self) -> None:  # noqa: N802 (name required by BaseHTTPRequestHandler)
        path = unquote(urlparse(self.path).path)

        if path == "/":
            self._handle_index()
        elif path == render.STYLESHEET_PATH:
            self._send(200, render.STYLESHEET, "text/css; charset=utf-8")
        elif path.startswith("/post/"):
            self._handle_post(path[len("/post/") :])
        else:
            self._send_not_found("Unknown page.")

    def _handle_index(self) -> None:
        try:
            posts = load_posts(self.posts_dir)
        except PostError as exc:
            self._send_error_page(exc)
            return
        self._send(200, render.render_index(posts))

    def _handle_post(self, slug: str) -> None:
        # Strip a trailing slash so /post/foo/ also works.
        slug = slug.rstrip("/")
        try:
            posts = load_posts(self.posts_dir)
        except PostError as exc:
            self._send_error_page(exc)
            return

        for post in posts:
            if post.slug == slug:
                self._send(200, render.render_post(post))
                return
        self._send_not_found(f"No post named {slug!r}.")

    def _send_not_found(self, message: str) -> None:
        self._send(404, render.render_not_found(message))

    def _send_error_page(self, exc: PostError) -> None:
        # A malformed post is a real error: show it, do not hide it.
        self._send(500, render.render_not_found(f"Could not load posts: {exc}"))

    def _send(
        self, status: int, body: str, content_type: str = "text/html; charset=utf-8"
    ) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, fmt: str, *args: object) -> None:
        # Keep the default concise access log, routed through print.
        print(f"[markblog] {self.address_string()} - {fmt % args}")


def make_server(
    host: str, port: int, posts_dir: Path
) -> ThreadingHTTPServer:
    """Create a server whose handler reads posts from ``posts_dir``."""
    handler = type("BoundBlogHandler", (BlogHandler,), {"posts_dir": posts_dir})
    return ThreadingHTTPServer((host, port), handler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local blog server.")
    parser.add_argument("--host", default="127.0.0.1", help="host to bind")
    parser.add_argument("--port", type=int, default=8000, help="port to bind")
    parser.add_argument(
        "--posts",
        type=Path,
        default=DEFAULT_POSTS_DIR,
        help="directory containing post .md files",
    )
    args = parser.parse_args(argv)

    posts_dir = args.posts.resolve()
    server = make_server(args.host, args.port, posts_dir)
    url = f"http://{args.host}:{args.port}/"
    print(f"markblog serving posts from {posts_dir}")
    print(f"Open {url} in your browser. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.server_close()
    return 0
