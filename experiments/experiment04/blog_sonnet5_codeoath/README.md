# blog

A small local blog. Write posts as Markdown files, run the app, read them as HTML.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python -m blog.main
```

Open http://127.0.0.1:5000/ in your browser. The main page lists all posts, newest first; click a title to read the full post.

## Write a Post

Add a new `.md` file to `posts/`. The filename becomes the URL (`posts/my-post.md` -> `/posts/my-post`).

```
---
title: "Post Title"
date: 2026-06-01
tags: [optional, tags]
---

Body in Markdown.
```

`title` and `date` are required. `tags` is optional; omit it for posts without tags. Restart the app (or reload, if the dev server is already tracking file changes) to see the new post.

## Tests

```bash
pytest
```

See `AGENTS.md` for the project's scope and rules, and `docs/decisions.md` for why things are built this way.
