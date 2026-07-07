"""A small, dependency-free Markdown to HTML renderer.

This supports a common subset of Markdown that covers typical blog posts:
headings, paragraphs, unordered and ordered lists, blockquotes, fenced code
blocks, horizontal rules, and the inline styles bold, italic, inline code,
links, and images. It is intentionally not a full CommonMark implementation;
the AGENTS.md "NOT" list makes that scope explicit.
"""

from __future__ import annotations

import html
import re

# Inline patterns, applied in order. Code spans are handled separately so their
# contents are never touched by the other inline rules.
_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_UL_ITEM = re.compile(r"^[-*+]\s+(.*)$")
_OL_ITEM = re.compile(r"^\d+\.\s+(.*)$")
_HR = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")
_FENCE = re.compile(r"^```(.*)$")


def render_markdown(text: str) -> str:
    """Convert a Markdown string to an HTML fragment."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    html_parts: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # Fenced code block: ``` ... ```
        fence = _FENCE.match(line)
        if fence:
            lang = fence.group(1).strip()
            code_lines: list[str] = []
            i += 1
            while i < n and not _FENCE.match(lines[i]):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence (or end of input)
            code = html.escape("\n".join(code_lines))
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            html_parts.append(f"<pre><code{cls}>{code}</code></pre>")
            continue

        # Blank line: nothing to emit between blocks.
        if line.strip() == "":
            i += 1
            continue

        # Horizontal rule.
        if _HR.match(line.strip()):
            html_parts.append("<hr>")
            i += 1
            continue

        # Heading.
        heading = _HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            content = _render_inline(heading.group(2).strip())
            html_parts.append(f"<h{level}>{content}</h{level}>")
            i += 1
            continue

        # Unordered list.
        if _UL_ITEM.match(line):
            items, i = _collect_list(lines, i, _UL_ITEM)
            html_parts.append(_render_list("ul", items))
            continue

        # Ordered list.
        if _OL_ITEM.match(line):
            items, i = _collect_list(lines, i, _OL_ITEM)
            html_parts.append(_render_list("ol", items))
            continue

        # Blockquote.
        if line.lstrip().startswith(">"):
            quote_lines: list[str] = []
            while i < n and lines[i].lstrip().startswith(">"):
                quote_lines.append(lines[i].lstrip()[1:].lstrip())
                i += 1
            inner = render_markdown("\n".join(quote_lines))
            html_parts.append(f"<blockquote>{inner}</blockquote>")
            continue

        # Paragraph: gather consecutive non-blank, non-block lines.
        para_lines: list[str] = []
        while i < n and lines[i].strip() != "" and not _starts_block(lines[i]):
            para_lines.append(lines[i].strip())
            i += 1
        content = _render_inline(" ".join(para_lines))
        html_parts.append(f"<p>{content}</p>")

    return "\n".join(html_parts)


def _starts_block(line: str) -> bool:
    """True if a line begins a new block, so it must not join a paragraph."""
    stripped = line.strip()
    return bool(
        _HEADING.match(line)
        or _UL_ITEM.match(line)
        or _OL_ITEM.match(line)
        or _FENCE.match(line)
        or _HR.match(stripped)
        or stripped.startswith(">")
    )


def _collect_list(
    lines: list[str], start: int, pattern: re.Pattern[str]
) -> tuple[list[str], int]:
    """Collect consecutive matching list items starting at index ``start``."""
    items: list[str] = []
    i = start
    while i < len(lines):
        match = pattern.match(lines[i])
        if not match:
            break
        items.append(match.group(1).strip())
        i += 1
    return items, i


def _render_list(tag: str, items: list[str]) -> str:
    rendered = "".join(f"<li>{_render_inline(item)}</li>" for item in items)
    return f"<{tag}>{rendered}</{tag}>"


def _render_inline(text: str) -> str:
    """Render inline Markdown, escaping HTML and protecting code spans."""
    placeholders: list[str] = []

    def _stash_code(match: re.Match[str]) -> str:
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00{len(placeholders) - 1}\x00"

    # Pull out `code spans` before escaping so their content stays literal.
    text = re.sub(r"`([^`]+)`", _stash_code, text)

    # Escape the remaining text, then apply inline styles on the safe string.
    text = html.escape(text, quote=False)

    text = _IMAGE.sub(
        lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}">', text
    )
    text = _LINK.sub(
        lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', text
    )
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITALIC.sub(r"<em>\1</em>", text)

    # Restore the protected code spans.
    def _restore(match: re.Match[str]) -> str:
        return placeholders[int(match.group(1))]

    return re.sub(r"\x00(\d+)\x00", _restore, text)
