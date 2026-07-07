# Decisions

## 2026-07-06: Flask for the web layer
**Status:** active
Flask is enough for two routes and a dev server. No need for anything heavier to run locally.

## 2026-07-06: Markdown files with YAML frontmatter as storage
**Status:** active
Posts are files in `posts/`, not database rows. A local, single-author blog does not need a database; a text editor is the whole authoring tool.

## 2026-07-06: python-frontmatter + PyYAML for metadata, Markdown for rendering
**Status:** active
`python-frontmatter` splits the YAML block from the Markdown body in one call instead of a hand-rolled string split. `Markdown` renders the body, with `fenced_code` and `tables` enabled since technical posts benefit from both.

## 2026-07-06: Filename is the slug, no separate ID field
**Status:** active
`posts/hello-world.md` becomes `/posts/hello-world`. One less field to keep in sync between the filename and the metadata.

## 2026-07-06: Malformed posts are skipped, not fatal
**Status:** active
A post missing `title` or `date`, or with broken YAML, is logged as a warning and left out of the listing instead of crashing the whole app. One bad file should not take down every other post.

## Known Risks

| Risk | Mitigation |
|---|---|
| A skipped post is only visible in the console log, not on the site itself | Acceptable for a single local author who runs the dev server themselves; revisit if the author is not the one running the server |
| Every request re-reads and re-parses all files in `posts/` | Fine at the size of a personal blog; add caching if the post count grows large enough to notice |
| Flask runs in debug mode via `app.run(debug=True)`, not meant for production | Out of scope: the request was for a local app |
