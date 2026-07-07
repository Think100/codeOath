---
title: "A Simple Way to Publish"
date: 2026-07-01
tags: [meta]
---

This blog has no build step and no external service. Start the app, and it
reads whatever is in `posts/` at that moment. Add a file, restart the app
(or just keep the debug server running), and the new post shows up on the
main page, newest first.

If a post file is missing its title or date, or its metadata cannot be
parsed, it is skipped and a warning is printed to the console. The rest of
the blog keeps working; one broken file does not take down the site.
