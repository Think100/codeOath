"""Infrastructure adapter: Markdown-to-HTML rendering using the `markdown` library."""

from __future__ import annotations

import markdown


class PythonMarkdownRenderer:
    """Implements MarkdownRenderer port using the python-markdown package."""

    def __init__(self) -> None:
        self._extensions = ["fenced_code", "codehilite", "tables", "toc"]

    def render(self, markdown_text: str) -> str:
        return markdown.markdown(markdown_text, extensions=self._extensions)
