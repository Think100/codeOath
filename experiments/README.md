# Experiments

## Why

codeOath claims that one extra line of guidance ("Follow the project structure described in README.md") changes how AI writes code: better structure, clearer boundaries, fewer silent failures. These experiments test that claim.

The hypothesis: AI agents default to the simplest possible structure. With minimal architectural guidance, they produce code that is better organized, handles errors more explicitly, and scales more cleanly, without losing features or readability.

These are not reference implementations. They are AI-generated programs compared side-by-side, with and without codeOath, to measure the delta.


## Test Cases

We use two prompts at different complexity levels. Each prompt is deliberately vague so the agent must make its own architectural decisions. The decisions it makes (or avoids) reveal how it thinks about structure.

### Simple: Desktop Note-Taking App

> Build me a small desktop note-taking app. I want to quickly jot down a thought, and it should still be there when I reopen the app. The window should be able to stay on top of other windows, and I want to control how transparent the window is. It should save automatically so I do not lose anything. Use Python.

Small scope, few files. A monolith is a defensible choice here.

**Decisions the agent must make:**

| Decision | What it reveals |
|---|---|
| Where to store notes (single file, folder, database) | Data model thinking |
| How to handle multiple notes vs. one note | Scope interpretation |
| When exactly to autosave (timer, on change, on close) | UX awareness |
| How to structure the code (one file, multiple files, layers) | Architecture instinct |
| Whether to add features not asked for (search, delete, font size) | Scope discipline |
| How to handle errors (file locked, disk full, corrupt data) | Robustness |

**Minimum viable result:**

- [ ] Window opens and displays text
- [ ] Text persists between sessions
- [ ] Always-on-top toggle works
- [ ] Transparency control works
- [ ] Autosave works without explicit user action
- [ ] No data loss on normal close

**Quality indicators:**

- [ ] Modified indicator (user knows if changes exist)
- [ ] Unsaved-changes protection on close
- [ ] Error feedback when save fails (no silent data loss)
- [ ] Clean separation of state from UI
- [ ] Dependency direction visible in imports
- [ ] Contracts in code (Protocol, interface, or equivalent)
- [ ] Proportional architecture (structure fits the problem size)


### Medium: Blog/CMS

> Build me a simple blog system. I want to write posts in Markdown, and they should be rendered as HTML pages. Each post needs a title, a date, and optional tags. I want a main page that lists all posts (newest first) and a page for each individual post. It should run locally as a web app. Use Python.

More moving parts, natural layer boundaries (HTTP, domain, persistence). Architecture choices matter here.

**Decisions the agent must make:**

| Decision | What it reveals |
|---|---|
| Web framework (Flask, FastAPI, none) | Dependency awareness |
| Where posts are stored (files, SQLite, both) | Data model thinking |
| Markdown parsing (library, custom parser) | Build vs. buy |
| How frontmatter is handled (YAML, custom format, DB fields) | Format design |
| Template engine (Jinja2, string formatting, custom) | Pragmatism |
| URL routing (/post/slug vs. /post/id vs. /post/date/title) | UX/API design |
| Whether an admin interface is built or not | Scope discipline |

**Minimum viable result:**

- [ ] Write posts in Markdown, display as HTML
- [ ] Main page lists all posts (newest first)
- [ ] Individual post page with rendered HTML
- [ ] Title, date, and tags per post
- [ ] Runs locally as a web app
- [ ] No data loss on restart

**Quality indicators:**

- [ ] Error feedback when a post cannot be loaded
- [ ] Clean separation: domain (post model) vs. web (routing) vs. persistence
- [ ] Tags are filterable (click a tag to see all posts with that tag)
- [ ] Dependency direction visible in imports
- [ ] Contracts in code (Protocol, interface, or equivalent)
- [ ] Proportional architecture (structure fits the problem size)


## Method

### How to Run

Give the AI agent the prompt. Do not add implementation details, architecture hints, or technology preferences.

Each prompt is run in two variants:
- **Reference:** The prompt as-is.
- **With codeOath:** The same prompt plus one line: "Follow the project structure described in README.md."

Same prompt, one extra line. That is the only variable.

### How to Evaluate

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| **Features complete** | Missing basics | All minimum features | Minimum + quality indicators |
| **Architecture** | Everything in one block | Some separation | Clear layers with direction |
| **Proportionality** | Over- or under-engineered | Acceptable | Structure matches problem size |
| **Error handling** | Silent failures | Errors shown to user | Errors shown + recovery |
| **Scope discipline** | Added unrequested features | Mostly on scope | Exactly what was asked |
| **Code clarity** | Hard to follow | Readable | Readable + self-documenting |

Score range: 0-12. The interesting comparison is not the absolute score but the delta between "with codeOath" and "without."

### Generation Time

How long each agent took to produce its result (wall clock, including file writes).

| Variant | Blog/CMS (Run 3) |
|---|---|
| Sonnet reference | 49s |
| Sonnet + codeOath | 171s |
| Opus reference | 90s |
| Opus + codeOath | 153s |

Run 1 and Run 2 times were not recorded. codeOath variants take 2-3.5x longer because the agents generate more files, write tests, and create documentation.


## What We Learned Across All Runs

**codeOath consistently changes architecture.** In every run, both models jump from monolith (0/2) to layered architecture (2/2) when given the codeOath reference. This is the most reliable effect.

**The effect depends on problem size.** For simple problems, codeOath can hurt (Opus over-engineers a 10-file note app). For medium problems with natural boundaries, codeOath helps both models equally (+2 each).

**Error handling is the universal weak spot.** No variant across any run scores 2/2 on error handling. The agents show errors to users (1/2) but never implement graceful recovery (skip the broken post, show the rest).

**Sonnet applies codeOath more proportionally than Opus.** Across all runs, Sonnet picks the right amount of structure for the problem size. Opus tends to build more layers than the problem needs, sometimes at the cost of basic features.


---


## Run 3: Blog/CMS (March 2026)

Test case: Medium. Prompt: Blog/CMS. Models: Sonnet 4, Opus 4. Evaluated by: Sonnet 4.

### Results

| Variant | Folder | Score | Architecture | Key Difference |
|---|---|---|---|---|
| Sonnet + codeOath | `experiment03/blog_sonnet_codeoath/` | **10/12** | 3-layer with Protocol | Clean ports-and-adapters, fail-fast on malformed posts |
| Opus + codeOath | `experiment03/blog_opus_codeoath/` | **9/12** | Full ports-and-adapters + Service | Two Protocols (Repo + Renderer), but silently skips bad posts |
| Sonnet reference | `experiment03/blog_sonnet_ref/` | **8/12** | Single file | Clean monolith, good code clarity, no layers |
| Opus reference | `experiment03/blog_opus_ref/` | **7/12** | Single file | Custom regex frontmatter parser, no contracts |

### Key Findings

**1. codeOath consistently adds +2 through architecture.** Both models jump from 0 (monolith) to 2 (clear layers with direction) when given the one-line codeOath reference. The delta is identical for Sonnet (+2) and Opus (+2). This is the single largest effect.

**2. Without codeOath, both models build a monolith.** Sonnet and Opus both default to a single `app.py` with everything mixed together. Neither introduces layer separation, Protocols, or dependency direction on its own. For a web app with natural boundaries (HTTP, domain, persistence), this is a missed opportunity.

**3. Medium complexity amplifies the architecture gap.** In Run 2 (simple note app), the architecture delta was less decisive because a monolith was a defensible choice. In Run 3 (blog with web framework, Markdown rendering, file parsing), the lack of separation in the reference versions is a real readability and maintainability cost.

**4. Error handling remains the universal weak spot.** All four variants score 1/2 on error handling. The codeOath versions surface errors more explicitly (RuntimeError on malformed posts) but none implement graceful recovery. The reference versions either silently fall back (Opus: date defaults to 2000-01-01) or crash with a generic 500.

**5. Opus + codeOath loses a point on scope discipline.** Opus added tests, docs/decisions.md, and docs/todo.md that were not requested. These are valuable in practice but the rubric asks for "exactly what was asked." Sonnet + codeOath also added these but scored higher on clarity, compensating in the total.

**6. No variant implemented tag filtering.** All four render tags as display-only spans. None added a `/tag/<name>` route. This was the most accessible quality indicator and would have required roughly 10 lines. Both codeOath variants noted it as a TODO rather than implementing it.

### Running the Programs

```bash
pip install flask markdown python-frontmatter pyyaml
python experiment03/blog_sonnet_codeoath/app.py
python experiment03/blog_sonnet_ref/app.py
python experiment03/blog_opus_codeoath/main.py
python experiment03/blog_opus_ref/app.py
```


## Run 2: Note-Taking App (March 2026)

Test case: Simple. Prompt: Note-Taking App. Models: Sonnet 4, Opus 4. Evaluated by: Sonnet 4.

### Results

| Variant | Folder | Score | Architecture | Key Difference |
|---|---|---|---|---|
| Sonnet + codeOath | `experiment02/note_sonnet_codeoath/` | **12/12** | 3-layer with Protocol | Only version with error feedback AND modified marker |
| Sonnet reference | `experiment02/note_sonnet_ref/` | **10/12** | Config + App + Main | Feature-complete, no layer separation |
| Opus reference | `experiment02/note_opus_ref/` | **7/12** | Single file | Persists window state, no error handling |
| Opus + codeOath | `experiment02/note_opus_codeoath/` | **6/12** | Full ports-and-adapters | 8 files, UI bypasses layers, no error handling |

### Key Findings

**1. Sonnet + codeOath is reproducibly the best result.** Full score in both runs. Right architecture dose, complete features, no silent failures.

**2. codeOath hurts Opus.** In both runs, Opus with codeOath builds more structure but forgets basics (error handling, modified marker). Without codeOath, Opus delivers a more functional program. The architecture instructions distract from the actual task.

**3. The biggest impact is on error handling.** The clearest difference between "with" and "without" codeOath is not folder structure but whether errors are surfaced to the user. The "Fail Fast" and "Feedback Loops" principles appear to have stronger effect than the architecture guidance.

### Running the Programs

```bash
python experiment02/note_sonnet_codeoath/main.py
python experiment02/note_sonnet_ref/main.py
python experiment02/note_opus_codeoath/main.py
python experiment02/note_opus_ref/sticky_note.py
```


## Run 1: Text Editor (March 2026)

Test case: Simple (variant). Prompt: Text Editor (not identical to Run 2). Models: Sonnet 4, Opus 4. This was the first run; prompts were not standardized yet.

### Results

| Variant | Folder | Files | Architecture | Features |
|---|---|---|---|---|
| Sonnet + codeOath | `experiment01/texteditor_sonnet/` | 4 | 3-layer with Protocol | Immutable state, modified tracking |
| Sonnet reference | `experiment01/texteditor_sonnet_ref/` | 1 | Single class | Most complete features, monolithic |
| Opus + codeOath | `experiment01/texteditor_opus/` | 10 | Full ports-and-adapters | Correct layers, missing basics |
| Opus reference | `experiment01/texteditor_opus_ref/` | 3 | Config + editor + main | Clean but feature-incomplete |

### Key Findings

**1. Architecture must be proportional to the problem.**
Opus with codeOath built 10 files with protocols, use cases, and a definition document, but forgot basic features like unsaved-changes protection. Sonnet with codeOath built 4 files with clean separation and delivered a more complete program. More structure is not always better structure.

**2. codeOath changes AI behavior.**
Without codeOath, both Sonnet and Opus defaulted to the simplest approach (1 file or flat class). With codeOath, both introduced layer separation, dependency direction, and contracts. The principles shifted the AI from "solve the task" to "solve the task within a maintainable structure."

**3. The right dose matters.**
Sonnet's interpretation (one file per layer, one Protocol for the boundary) was the best balance of structure and function. It applied the principles proportionally to the problem size. This confirms codeOath's Principle 4: "Maintenance must be cheap."

### Caveats

- The prompts were not identical. Opus was explicitly told to use full ports-and-adapters; Sonnet was told to "structure sensibly." This likely pushed Opus toward over-engineering.
- These are single runs, not a controlled experiment. Results may vary.
- All code was generated by AI sub-agents (Haiku, Sonnet, Opus) in March 2026.

### Running the Programs

All programs use Python 3.14+ with tkinter (included in standard Python).

```bash
python experiment01/texteditor_sonnet/main.py
python experiment01/texteditor_sonnet_ref/editor.py
python experiment01/texteditor_opus/main.py
python experiment01/texteditor_opus_ref/main.py
```
