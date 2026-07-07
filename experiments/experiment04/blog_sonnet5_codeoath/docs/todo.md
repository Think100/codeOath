# TODO

## Tasks
- [ ] None open right now; core features (write in Markdown, list newest first, per-post page) are done

## Open Questions
- [ ] Should skipped (malformed) posts also show a visible warning somewhere on the site itself, not just in the console log?
      Context: right now the only trace is the server log; a local single-author blog may never need more than that
      Priority: revisit if posts start being edited by someone other than the person running the server

## Resolved
- [x] Flask or something lighter (http.server)? -> Flask (routing and templating without hand-rolling both)
- [x] Where do posts live? -> posts/*.md, filename is the slug
- [x] What happens to a post with bad metadata? -> skipped with a logged warning, rest of the site keeps working
