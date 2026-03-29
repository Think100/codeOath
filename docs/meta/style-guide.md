# Documentation Style Guide

Rules for all files in `docs/`. Goal: every document looks like it belongs to the same project. Simple, scannable, timeless.


## File Structure

Every document follows this skeleton:

```
> [README](../README.md) > **Document Title**        <- breadcrumb (line 1)
                                                       <- blank line
# Document Title                                       <- H1 (same as breadcrumb title)
                                                       <- blank line
One-sentence summary of what this document is and who   <- intro line
should read it.
                                                       <- blank line
## First Section                                       <- H2 for main sections
                                                       <- blank line
### Subsection                                         <- H3 for subsections within a section
```

### Breadcrumb

Line 1 of every file except `docs/README.md` (which is the docs root).

**Depth 1** (files directly in `docs/`):
```
> [README](../README.md) > **Stage 1: Start**
```

**Depth 2** (files in `docs/resources/`, `docs/languages/`):
```
> [README](../../README.md) > [Docs](../) > **Ports and Adapters**
```

**Meta files** (`docs/meta/`): no breadcrumb. These are internal project files, not user-facing docs.


### TL;DR Block

Documents longer than ~100 lines should open with a TL;DR block right after the H1 title. Format:

```markdown
> **TL;DR** -- Three things this document tells you: (1) separate domain from adapters,
> (2) write down decisions, (3) commit after each step.
```

For deep-dive, reference, or practical-guide documents, integrate the document type into the TL;DR prefix:

```markdown
> **TL;DR (deep dive)** -- Domain defines what it needs (ports). Adapters provide it. ...
> **TL;DR (practical guide)** -- Let AI write tests, you review, then AI implements. ...
> **TL;DR (reference)** -- When domain/ grows too large: feature-sliced, modular monolith, ...
```

One blockquote per document, not two. The type tag in parentheses replaces the separate intro blockquote.

The TL;DR is a blockquote with bold prefix. It gives the reader the 3-5 key points in 2-3 lines. If the reader never scrolls past the TL;DR, they should still understand the gist.

### Intro Line

After the TL;DR, one sentence that answers: "What is this and who needs it?" No blockquote, no bold, just a plain sentence.

```markdown
# Stage 2: Grow

> **TL;DR** -- (1) Split your code...

When your project outgrows Stage 1, this guide shows you how to add structure without adding bureaucracy.
```


### Headings

- **H1 (`#`):** Document title. Exactly one per file.
- **H2 (`##`):** Main sections. These are what a reader scans.
- **H3 (`###`):** Subsections within an H2. Use sparingly.
- **H4+ (`####`):** Avoid. If you need H4, the document is too deep. Split into sections or separate files.


## Blockquote Types

Blockquotes serve four purposes. Distinguish them by the first word or phrase:

### 1. TL;DR (at document top only)

```markdown
> **TL;DR** -- Set up in 10 minutes, maintain in 2 minutes per session.
> **TL;DR (deep dive)** -- Domain defines what it needs (ports). ...
```

### 2. AI Prompt (user copies this to their AI)

Always introduced by a line like "Give your AI this prompt:" or "Ask your AI:". The prompt itself is a blockquote:

```markdown
Give your AI this prompt:

> "Read my AGENTS.md and create the folder structure described there."
```

### 3. Analogy or Explanation

For making abstract concepts concrete. Use when a metaphor helps:

```markdown
> Think of ports like electrical outlets. The outlet shape is the contract.
> What you plug in (lamp, charger, toaster) is the adapter.
```

### 4. Warning

For things that can go wrong or are dangerous. Start with **Warning:**

```markdown
> **Warning:** This prompt tells the AI to attack your own code. Only run it on your own projects.
```


## Code Blocks

### Language Tags

Always use a language tag. No bare triple-backticks.

| Content | Tag |
|---|---|
| Python | ` ```python ` |
| TOML (pyproject.toml) | ` ```toml ` |
| YAML | ` ```yaml ` |
| JSON | ` ```json ` |
| SQL | ` ```sql ` |
| Bash / shell commands | ` ```bash ` |
| Markdown examples | ` ```markdown ` |
| Folder/directory trees | ` ```text ` |
| Language-neutral pseudocode | ` ```text ` |
| Generic / no syntax highlighting needed | ` ```text ` |

### Folder Trees

Use `text` tag. Use Unicode box-drawing characters:

```text
myproject/
├── src/
│   ├── domain/
│   │   └── models.py
│   └── adapters/
│       └── db.py
└── tests/
```


## Links and Cross-References

### Relative Paths

Always use relative paths. Never absolute paths or URLs to the same repo.

```markdown
See [grow.md](grow.md) for details.
```

### Link Text

Plain text, no backticks in link text:

```markdown
Good: See [ports-and-adapters.md](resources/ports-and-adapters.md)
Bad:  See [`ports-and-adapters.md`](resources/ports-and-adapters.md)
```

### Section Anchors

Use when linking to a specific section in another file:

```markdown
See the [NOT field](start.md#the-not-field) section.
```


## Lists

- Use `-` for bullet points (not `*` or `+`)
- Use `- [ ]` for checklists
- One blank line before a list, no blank lines between items


## What NOT to Do

- No emoji in any document
- No em-dashes. Use commas, semicolons, or `--`
- No `<details>/<summary>` in docs/ files (only in README.md where GitHub rendering is guaranteed)
- No table of contents in individual files (they are short enough to scan)
- No badges or shields
- No front matter (YAML or otherwise)


## Vibe Coder Sections

Vibe coders do not read documentation. They copy, try, fail, and copy again. The best developer tools understand this: they show results, not explanations. codeOath docs should do the same.

Sections aimed at beginners or vibe coders should be recognizable by tone, not by markers. The pattern:

1. **Start with the problem** the reader has (not the concept they need to learn)
2. **Give an AI prompt** they can copy
3. **Show what the result looks like** (code example, folder tree, or before/after comparison)
4. **Explain why** only if it is not obvious

Do not label sections as "for beginners" or "for vibe coders". The content should be accessible without a label.

### Show, Don't Explain

Prefer a before/after code block over a paragraph of explanation:

```markdown
**Before** (everything in one file):
(code block showing messy code)

**After** (domain separated from adapters):
(code block showing clean code)
```

Three seconds of looking at a before/after teaches more than three paragraphs of text.

### Prompts Must Be Findable

AI prompts are the most valuable content for vibe coders. They must not drown in surrounding text. Rules:

- Always introduce a prompt with a short line: "Give your AI this prompt:" or "Ask your AI:"
- The prompt is always a blockquote (visually distinct from body text)
- Keep the prompt self-contained (a reader should be able to copy it without reading the surrounding text)


## Checklist for New or Edited Documents

Before committing changes to any file in `docs/`:

- [ ] Breadcrumb on line 1 (except meta/ files and README.md)
- [ ] Exactly one H1, matching the breadcrumb title
- [ ] Intro line after H1
- [ ] All code blocks have language tags
- [ ] Folder trees use `text` tag
- [ ] No bare blockquotes (each has a clear type: intro, prompt, analogy, warning)
- [ ] Links use relative paths, no backticks in link text
- [ ] Bullets use `-`
- [ ] No emoji, no em-dashes, no `<details>` tags
