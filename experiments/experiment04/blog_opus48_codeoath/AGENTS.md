# markblog

Local web app that turns Markdown files into a small blog. You write posts as
Markdown files with a title, date, and optional tags. The app renders them to
HTML: one index page listing all posts (newest first) and one page per post.

## NOT
- Not a static site generator (serves live, no build/deploy step)
- Not a CMS (no admin UI, no login, posts are plain files on disk)
- Not a public web server (local use only, not hardened for the internet)
- Not a Markdown superset (supports a common subset, not every extension)
- No database (posts live in posts/ as .md files)

## Rules
- Python 3.10+
- Standard library only (no third-party dependencies)
- Code and comments in English
- Never overwrite or delete a user's post files
- Errors must be visible, never hide them silently
- New files: ask first (AI rule)
- New dependencies: ask first, explain why (AI rule)
- When uncertain: ask, don't guess (AI rule)

## Structure
- Source: src/blog/
- Entry point: run.py
- Posts (content): posts/
- Tests: tests/
- Docs: docs/
- Tasks and open questions: docs/todo.md

## Post format
Each post is a `.md` file in `posts/` with a front matter header:

    ---
    title: My first post
    date: 2026-06-01
    tags: intro, meta
    ---

    Markdown content goes here.

- `title` (required): shown as the post heading and in the list
- `date` (required): `YYYY-MM-DD`, used to sort newest first
- `tags` (optional): comma-separated, shown as labels
- The file name (without `.md`) is the URL slug
