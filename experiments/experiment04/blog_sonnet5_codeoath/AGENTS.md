# blog

A local web app that turns Markdown files into a blog: a main page listing
all posts newest first, and one page per post.

## NOT
- Not multi-user or accounts (single local author, no login needed)
- Not database-backed (posts are Markdown files on disk; no DB needed for a local, single-author blog)
- Not a production deployment (runs locally via Flask's dev server, as requested)
- Not a WYSIWYG editor (posts are written and edited as Markdown files directly)
- Not comments or any interactivity (not requested; would add spam handling, storage, and moderation)

## Rules
- Python 3.11+
- Code and comments in English
- Never overwrite a post file from the app (the app only reads posts, never writes them)
- No secrets in code or version control
- Errors must be visible: a malformed post is skipped with a logged warning, never silently dropped without a trace
- New files: ask first (AI rule)
- New dependencies: ask first, explain why (AI rule)
- Commit after each completed task (AI rule)
- When uncertain: ask, don't guess (AI rule)

## Architecture
domain/    Post model, validation, "newest first" sort rule. No external imports.
adapters/  FileSystemPostRepository (reads posts/*.md) and the Flask web layer (routes, templates).
main.py    Composition root: creates the repository, wires it into the Flask app, starts the server.

Rule: adapters may use domain. Domain must never use adapters.

## Structure
- Source: blog/ (domain/, adapters/, main.py)
- Content: posts/ (one Markdown file per post, YAML frontmatter: title, date, tags)
- Templates: templates/
- Static assets: static/
- Tests: tests/
- Docs: docs/
- Tasks and open questions: docs/todo.md
- Decisions: docs/decisions.md

## Post Format
```
---
title: "Post Title"
date: 2026-06-01
tags: [optional, tags]
---

Body in Markdown.
```
`title` and `date` are required. `tags` is optional.
