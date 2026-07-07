# Papertrail

A small local blog. Posts are Markdown files with a YAML metadata block;
the app renders them as HTML pages with a front page (newest first),
one page per post, and tag filtering.

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Write a post

Create `posts/<slug>.md`:

```markdown
---
title: My new post
date: 2026-07-06
tags: [python, notes]   # optional
---
Markdown body goes here.
```

Save and refresh the browser; posts are re-read on every request.
Files with broken metadata are skipped and listed in a warning on the
front page instead of taking the blog down.

## Tests

```bash
pytest
```

## Structure

See [AGENTS.md](AGENTS.md) for the project definition, rules, and layout.
In short: `src/domain/` holds the post model and queries, `src/adapters/`
holds file loading, Markdown rendering, and the Flask routes; `app.py`
wires them together.
