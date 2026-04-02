# Experiments

## Why

codeOath claims that one extra line of guidance ("Follow the project structure described in README.md") changes how AI writes code: better structure, clearer boundaries, fewer silent failures. These experiments test that claim.

The hypothesis: AI agents default to the simplest possible structure. With minimal architectural guidance, they produce code that is better organized, handles errors more explicitly, and scales more cleanly, without losing features or readability.

These are not reference implementations. They are AI-generated programs compared side-by-side, with and without codeOath, to measure the delta.


## Results

All experiments were run with Claude Sonnet 4.6 and Claude Opus 4.6 in March 2026. AI model behavior changes over time. Results with newer models or different providers may differ.

| Run | Test Case | Best Variant | Score | Worst Variant | Score | Key Delta |
|---|---|---|---|---|---|---|
| 3 | Blog/CMS (medium) | Sonnet + codeOath | 10/12 | Opus reference | 7/12 | +2 architecture in both models |
| 2 | Note-Taking App (simple) | Sonnet + codeOath | 12/12 | Opus + codeOath | 6/12 | codeOath hurts Opus on simple tasks |
| 1 | Text Editor (simple) | Sonnet + codeOath | best | Opus + codeOath | worst | Architecture must be proportional |

**Pattern:** Sonnet + codeOath wins every run. Opus + codeOath over-engineers simple problems but benefits from guidance on medium complexity.


## What We Learned Across All Runs

**codeOath consistently changes architecture.** In every run, both models jump from monolith to layered architecture when given the codeOath reference. This is the most reliable effect.

**The effect depends on problem size.** For simple problems, codeOath can hurt (Opus over-engineers a 10-file note app). For medium problems with natural boundaries, codeOath helps both models equally.

**Error handling is the universal weak spot.** No variant across any run scores 2/2 on error handling. The agents show errors to users but never implement graceful recovery (skip the broken post, show the rest).

**Sonnet applies codeOath more proportionally than Opus.** Across all runs, Sonnet picks the right amount of structure for the problem size. Opus tends to build more layers than the problem needs, sometimes at the cost of basic features.


## Method

### Prompts

Each test case uses a deliberately vague prompt so the agent must make its own architectural decisions. The decisions it makes (or avoids) reveal how it thinks about structure.

Each prompt is run in two variants:
- **Reference:** The prompt as-is.
- **With codeOath:** The same prompt plus one line: "Follow the project structure described in README.md."

Same prompt, one extra line. That is the only variable.

#### Simple Task: Desktop Note-Taking App

> Build me a small desktop note-taking app. I want to quickly jot down a thought, and it should still be there when I reopen the app. The window should be able to stay on top of other windows, and I want to control how transparent the window is. It should save automatically so I do not lose anything. Use Python.

#### Medium Task: Blog/CMS

> Build me a simple blog system. I want to write posts in Markdown, and they should be rendered as HTML pages. Each post needs a title, a date, and optional tags. I want a main page that lists all posts (newest first) and a page for each individual post. It should run locally as a web app. Use Python.

### Evaluation Criteria

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

How long each agent took to produce its result (wall clock, including file writes). codeOath variants take 2-3.5x longer because the agents generate more files, write tests, and create documentation.

| Variant | Blog/CMS (Run 3) |
|---|---|
| Sonnet reference | 49s |
| Sonnet + codeOath | 171s |
| Opus reference | 90s |
| Opus + codeOath | 153s |

Run 1 and Run 2 times were not recorded.


---


## Run 3: Blog/CMS (March 2026)

Models: Sonnet 4.6, Opus 4.6. Evaluated by: Sonnet 4.6. codeOath version: Beta.

### Results

| Variant | Folder | Score | Architecture | Key Difference |
|---|---|---|---|---|
| Sonnet + codeOath | `experiment03/blog_sonnet_codeoath/` | **10/12** | 3-layer with Protocol | Clean ports-and-adapters, fail-fast on malformed posts |
| Opus + codeOath | `experiment03/blog_opus_codeoath/` | **9/12** | Full ports-and-adapters + Service | Two Protocols (Repo + Renderer), but silently skips bad posts |
| Sonnet reference | `experiment03/blog_sonnet_ref/` | **8/12** | Single file | Clean monolith, good code clarity, no layers |
| Opus reference | `experiment03/blog_opus_ref/` | **7/12** | Single file | Custom regex frontmatter parser, no contracts |

### Learnings

1. **codeOath consistently adds +2 through architecture.** Both models jump from 0 (monolith) to 2 (clear layers with direction). The delta is identical for Sonnet and Opus.
2. **Without codeOath, both models build a monolith.** Neither introduces layer separation, Protocols, or dependency direction on its own.
3. **Medium complexity amplifies the architecture gap.** In Run 2 (simple note app), a monolith was defensible. Here, the lack of separation is a real readability and maintainability cost.
4. **Error handling remains the universal weak spot.** All four variants score 1/2. codeOath versions surface errors more explicitly (RuntimeError on malformed posts) but none implement graceful recovery.
5. **Opus + codeOath loses a point on scope discipline.** Opus added tests, docs/decisions.md, and docs/todo.md that were not requested.
6. **No variant implemented tag filtering.** All four render tags as display-only spans. This was the most accessible quality indicator and would have required roughly 10 lines.

### Running the Programs

```bash
pip install flask markdown python-frontmatter pyyaml
python experiment03/blog_sonnet_codeoath/app.py
python experiment03/blog_sonnet_ref/app.py
python experiment03/blog_opus_codeoath/main.py
python experiment03/blog_opus_ref/app.py
```


## Run 2: Note-Taking App (March 2026)

Models: Sonnet 4.6, Opus 4.6. Evaluated by: Sonnet 4.6. codeOath version: Beta.

### Results

| Variant | Folder | Score | Architecture | Key Difference |
|---|---|---|---|---|
| Sonnet + codeOath | `experiment02/note_sonnet_codeoath/` | **12/12** | 3-layer with Protocol | Only version with error feedback AND modified marker |
| Sonnet reference | `experiment02/note_sonnet_ref/` | **10/12** | Config + App + Main | Feature-complete, no layer separation |
| Opus reference | `experiment02/note_opus_ref/` | **7/12** | Single file | Persists window state, no error handling |
| Opus + codeOath | `experiment02/note_opus_codeoath/` | **6/12** | Full ports-and-adapters | 8 files, UI bypasses layers, no error handling |

### Learnings

1. **Sonnet + codeOath is reproducibly the best result.** Full score in both runs. Right architecture dose, complete features, no silent failures.
2. **codeOath hurts Opus.** In both runs, Opus with codeOath builds more structure but forgets basics (error handling, modified marker). Without codeOath, Opus delivers a more functional program.
3. **The biggest impact is on error handling.** The clearest difference between "with" and "without" codeOath is not folder structure but whether errors are surfaced to the user. The "Fail Fast" and "Feedback Loops" principles appear to have stronger effect than the architecture guidance.

### Running the Programs

```bash
python experiment02/note_sonnet_codeoath/main.py
python experiment02/note_sonnet_ref/main.py
python experiment02/note_opus_codeoath/main.py
python experiment02/note_opus_ref/sticky_note.py
```


## Run 1: Text Editor (March 2026)

Models: Sonnet 4.6, Opus 4.6. codeOath version: Beta. This was the first run; prompts were not standardized yet.

**Caveat:** The prompts were not identical. Opus was explicitly told to use full ports-and-adapters; Sonnet was told to "structure sensibly." This likely pushed Opus toward over-engineering. These are single runs, not a controlled experiment.

### Results

| Variant | Folder | Files | Architecture | Features |
|---|---|---|---|---|
| Sonnet + codeOath | `experiment01/texteditor_sonnet/` | 4 | 3-layer with Protocol | Immutable state, modified tracking |
| Sonnet reference | `experiment01/texteditor_sonnet_ref/` | 1 | Single class | Most complete features, monolithic |
| Opus + codeOath | `experiment01/texteditor_opus/` | 10 | Full ports-and-adapters | Correct layers, missing basics |
| Opus reference | `experiment01/texteditor_opus_ref/` | 3 | Config + editor + main | Clean but feature-incomplete |

### Learnings

1. **Architecture must be proportional to the problem.** Opus with codeOath built 10 files with protocols, use cases, and a definition document, but forgot basic features like unsaved-changes protection. Sonnet with codeOath built 4 files with clean separation and delivered a more complete program.
2. **codeOath changes AI behavior.** Without codeOath, both models defaulted to the simplest approach. With codeOath, both introduced layer separation, dependency direction, and contracts.
3. **The right dose matters.** Sonnet's interpretation (one file per layer, one Protocol for the boundary) was the best balance of structure and function. This confirms codeOath's Principle 4: "Maintenance must be cheap."

### Running the Programs

All programs use Python 3.14+ with tkinter (included in standard Python).

```bash
python experiment01/texteditor_sonnet/main.py
python experiment01/texteditor_sonnet_ref/editor.py
python experiment01/texteditor_opus/main.py
python experiment01/texteditor_opus_ref/main.py
```
