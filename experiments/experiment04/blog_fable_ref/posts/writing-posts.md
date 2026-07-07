---
title: How to Write a Post
date: 2026-07-01
tags: guide
---

Create a new `.md` file in the `posts/` directory. The filename becomes the
URL slug, so `my-trip.md` is served at `/post/my-trip`.

Every post starts with a front matter block:

```
---
title: My Trip to the Alps
date: 2026-07-15
tags: travel, hiking
---
```

| Field | Required | Format                          |
| ----- | -------- | ------------------------------- |
| title | yes      | free text                       |
| date  | yes      | YYYY-MM-DD                      |
| tags  | no       | comma-separated list            |

Everything after the second `---` is the post body in regular Markdown.
No restart needed; posts are re-read on every request.
