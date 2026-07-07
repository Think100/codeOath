# Markdown Blog

A minimal blog engine. Write posts as Markdown files, run a local Flask app,
get a list page and a page per post.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open http://127.0.0.1:5000 in a browser.

## Writing a post

Add a `.md` file to `posts/`. The filename (without `.md`) becomes the
post's URL slug, e.g. `posts/my-trip.md` becomes `/post/my-trip`.

Each file needs a frontmatter block at the top with `title` and `date`
(format `YYYY-MM-DD`). `tags` is optional and comma-separated:

```markdown
---
title: My Trip
date: 2026-03-01
tags: travel, notes
---

The rest of the file is regular **Markdown**.
```

Posts without a valid `title`/`date` are skipped (with a warning printed
to the console) instead of crashing the site.

## Project layout

```
app.py              Flask routes (index page, post page, 404)
blog.py             Loads posts/*.md, parses frontmatter, renders Markdown
posts/              Your posts, one .md file each
templates/           Jinja2 templates (base, index, post, 404)
static/style.css     Styling
requirements.txt
```

## Assumptions

- Posts are local Markdown files, not stored in a database.
- Frontmatter is a simple `key: value` block, not full YAML, so no extra
  dependency beyond Flask and Markdown was needed.
- `date` must be `YYYY-MM-DD`; there's no timezone handling.
- The Flask development server (`app.run(debug=True)`) is used since this
  is meant to run locally, not be deployed to production.
- Three example posts are included in `posts/` to demonstrate the format,
  including one without tags to show that they're optional.
