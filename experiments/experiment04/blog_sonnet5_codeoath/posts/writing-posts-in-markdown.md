---
title: "Writing Posts in Markdown"
date: 2026-06-15
tags: [meta, markdown]
---

Every post is a `.md` file in the `posts/` folder. The filename becomes the
post's web address, so `writing-posts-in-markdown.md` is served at
`/posts/writing-posts-in-markdown`.

The top of the file holds the metadata:

```yaml
---
title: "Your Title"
date: 2026-06-15
tags: [tag-one, tag-two]
---
```

`title` and `date` are required. `tags` is optional; leave it out entirely
if a post has none. Everything below the second `---` is the post body,
written in regular Markdown: headings, **bold**, *italics*, lists, code
blocks, and tables all work.
