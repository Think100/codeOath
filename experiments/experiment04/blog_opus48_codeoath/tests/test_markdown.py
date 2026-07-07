"""Tests for the Markdown renderer."""

from blog.markdown import render_markdown


def test_heading_levels():
    assert render_markdown("# Title") == "<h1>Title</h1>"
    assert render_markdown("### Sub") == "<h3>Sub</h3>"


def test_paragraph_joins_wrapped_lines():
    assert render_markdown("one\ntwo") == "<p>one two</p>"


def test_blank_line_separates_paragraphs():
    html = render_markdown("first\n\nsecond")
    assert html == "<p>first</p>\n<p>second</p>"


def test_bold_and_italic():
    assert render_markdown("**b**") == "<p><strong>b</strong></p>"
    assert render_markdown("*i*") == "<p><em>i</em></p>"


def test_inline_code_is_not_styled_and_is_escaped():
    html = render_markdown("use `a < b && c` here")
    assert "<code>a &lt; b &amp;&amp; c</code>" in html


def test_link_and_image():
    assert '<a href="https://x.com">x</a>' in render_markdown("[x](https://x.com)")
    assert '<img src="/p.png" alt="pic">' in render_markdown("![pic](/p.png)")


def test_unordered_list():
    html = render_markdown("- a\n- b")
    assert html == "<ul><li>a</li><li>b</li></ul>"


def test_ordered_list():
    html = render_markdown("1. a\n2. b")
    assert html == "<ol><li>a</li><li>b</li></ol>"


def test_fenced_code_block_preserves_and_escapes():
    html = render_markdown("```python\nx = 1 < 2\n```")
    assert '<pre><code class="language-python">x = 1 &lt; 2</code></pre>' == html


def test_blockquote():
    html = render_markdown("> quoted")
    assert html == "<blockquote><p>quoted</p></blockquote>"


def test_horizontal_rule():
    assert render_markdown("---") == "<hr>"


def test_raw_html_in_text_is_escaped():
    html = render_markdown("a <script>alert(1)</script> b")
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
