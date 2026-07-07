"""HTML page templates for the blog.

Small string templates only; the post body itself is rendered to HTML by the
Markdown module. Titles and tags are HTML-escaped here because they come from
user-supplied front matter.
"""

from __future__ import annotations

import html

from .posts import Post

STYLESHEET_PATH = "/static/style.css"


def _page(title: str, body: str) -> str:
    """Wrap a body fragment in the shared HTML skeleton."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{STYLESHEET_PATH}">
</head>
<body>
<div class="wrap">
{body}
<footer><a href="/">&larr; All posts</a></footer>
</div>
</body>
</html>
"""


def _tags_html(tags: list[str]) -> str:
    if not tags:
        return ""
    labels = "".join(
        f'<span class="tag">{html.escape(tag)}</span>' for tag in tags
    )
    return f'<div class="tags">{labels}</div>'


def render_index(posts: list[Post], site_title: str = "My Blog") -> str:
    """Render the index page listing all posts, newest first."""
    if posts:
        items = []
        for post in posts:
            items.append(
                f'<li class="post-item">'
                f'<a class="post-link" href="/post/{html.escape(post.slug)}">'
                f"{html.escape(post.title)}</a>"
                f'<div class="meta"><time>{html.escape(post.date_display)}'
                f"</time></div>"
                f"{_tags_html(post.tags)}"
                f"</li>"
            )
        listing = '<ul class="post-list">' + "".join(items) + "</ul>"
    else:
        listing = '<p class="empty">No posts yet. Add a .md file to posts/.</p>'

    body = f"<header><h1>{html.escape(site_title)}</h1></header>\n{listing}"
    # The index has no need for the "all posts" footer link back to itself,
    # but keeping one skeleton keeps the code simple; hide it via body only.
    return _page(site_title, body)


def render_post(post: Post) -> str:
    """Render a single post page."""
    body = (
        f"<article>"
        f"<header>"
        f"<h1>{html.escape(post.title)}</h1>"
        f'<div class="meta"><time>{html.escape(post.date_display)}</time></div>'
        f"{_tags_html(post.tags)}"
        f"</header>"
        f'<div class="content">{post.html}</div>'
        f"</article>"
    )
    return _page(post.title, body)


def render_not_found(message: str = "Page not found") -> str:
    """Render a 404 page."""
    body = (
        f'<header><h1>404</h1></header>'
        f"<p>{html.escape(message)}</p>"
    )
    return _page("Not found", body)


STYLESHEET = """\
:root {
  --fg: #1a1a1a;
  --muted: #6a6a6a;
  --accent: #2563eb;
  --bg: #ffffff;
  --code-bg: #f4f4f5;
  --border: #e5e5e5;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font: 17px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: var(--fg);
  background: var(--bg);
}
.wrap { max-width: 720px; margin: 0 auto; padding: 3rem 1.25rem 4rem; }
header h1 { font-size: 2rem; line-height: 1.2; margin: 0 0 .25rem; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.meta { color: var(--muted); font-size: .9rem; margin: .25rem 0; }
.tags { margin: .5rem 0; display: flex; flex-wrap: wrap; gap: .4rem; }
.tag {
  display: inline-block;
  background: var(--code-bg);
  color: var(--muted);
  border-radius: 999px;
  padding: .1rem .6rem;
  font-size: .8rem;
}
.post-list { list-style: none; padding: 0; margin: 2rem 0 0; }
.post-item { padding: 1.1rem 0; border-bottom: 1px solid var(--border); }
.post-link { font-size: 1.25rem; font-weight: 600; }
.empty { color: var(--muted); }
article .content { margin-top: 1.5rem; }
article h1, article h2, article h3 { line-height: 1.25; }
pre {
  background: var(--code-bg);
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
}
code {
  background: var(--code-bg);
  padding: .1rem .35rem;
  border-radius: 4px;
  font-size: .9em;
}
pre code { background: none; padding: 0; }
blockquote {
  margin: 1rem 0;
  padding: .25rem 1rem;
  border-left: 3px solid var(--border);
  color: var(--muted);
}
img { max-width: 100%; height: auto; }
hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border); }
"""
