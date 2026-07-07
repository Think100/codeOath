# Simple Markdown Blog

A small local blog system. You write posts in Markdown, and the app renders them
as HTML pages: a home page listing all posts (newest first) and one page per
post.

## Features

- Posts written in Markdown with YAML front matter (`title`, `date`, optional `tags`)
- Home page listing every post, newest first
- A dedicated page for each post
- Fenced code blocks with syntax highlighting, tables, and blockquotes
- Runs locally as a Flask web app

## Requirements

- Python 3.10 or newer

## Setup

```bash
# From inside this folder:
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open <http://127.0.0.1:5000/> in your browser.

The app reads posts from disk on every request, so while it is running you can
edit a post or add a new one and just refresh the page to see the change.

## Writing a post

Create a new `.md` file in the `posts/` folder. Start it with a front matter
block, then write the body in Markdown:

```markdown
---
title: My New Post
date: 2026-07-06
tags: [python, notes]
---

The body of the post goes here.
```

Notes:

- `title` and `date` are required. `date` uses ISO format (`YYYY-MM-DD`).
- `tags` is optional. Use a YAML list (`[a, b]`) or a comma-separated string
  (`a, b`).
- The file name (without `.md`) becomes the URL slug. For example,
  `my-new-post.md` is served at `/posts/my-new-post/`.
- Posts are sorted by date, newest first.

## Project layout

```
app.py             Flask application and Markdown loading
requirements.txt   Python dependencies
posts/             Markdown source files (one per post)
templates/         Jinja2 HTML templates
static/            CSS
```
