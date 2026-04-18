# Documentation

## How to Read This

Three paths depending on what you need:

| You want to... | Start here |
|---|---|
| Set up a new project | [start.md](start.md) |
| Fix a messy existing project | [triggers.md](resources/triggers.md#already-have-a-project-refactoring) |
| Understand the principles | [philosophy.md](resources/philosophy.md) |


## The Three Stages

Stage 1 is enough for most projects. Only add more structure when something starts going wrong.

| Stage | When | What |
|---|---|---|
| **1. [Start](start.md)** | Any project | AGENTS.md + todo.md |
| **2. [Grow](grow.md)** | Things get messy | Domain/adapters, decisions, ports, testing |
| **3. [Enforce](enforce.md)** | Rules keep getting broken | Linters, import checks, CI/CD |
| **[AI Workflow](ai-workflow.md)** | Any stage | Multi-perspective reviews, session habits, reusable agents |

Not sure if you should move stage? Check the [triggers](resources/triggers.md).


## Resources

Everything that is not part of the core path. Look things up when you need them.

| Document | What it covers |
|---|---|
| [triggers.md](resources/triggers.md) | When to move between stages (symptom table) |
| [prompts.md](resources/prompts.md) | All copy-paste AI prompts on one page |
| [ai-code-review.md](resources/ai-code-review.md) | Multi-perspective review workflow before commits and PRs |
| [auto-documentation.md](resources/auto-documentation.md) | Generate developer docs and Mermaid diagrams from your codebase |
| [domain-and-adapters.md](resources/domain-and-adapters.md) | The architecture pattern behind Stage 2 |
| [architecture-patterns.md](resources/architecture-patterns.md) | Feature-sliced, modular monolith, vertical slices |
| [testing.md](resources/testing.md) | How testing works, TDD with AI, what to test |
| [dependency-evaluation.md](resources/dependency-evaluation.md) | How to evaluate and add third-party dependencies safely |
| [security.md](resources/security.md) | Input validation, secrets, auth, common vulnerabilities |
| [performance.md](resources/performance.md) | Database, caching, timeouts, crash recovery |
| [build-pipeline.md](resources/build-pipeline.md) | Local build pipeline, reproducible builds, release automation |
| [release-checklist.md](resources/release-checklist.md) | What to check before publishing a project |
| [language-conventions.md](resources/language-conventions.md) | Which language to use where (code, comments, docs, commits) |
| [philosophy.md](resources/philosophy.md) | Five principles, Pace Layers, why codeOath works |


## Language Guides

How codeOath concepts translate to specific languages.

| Language | File |
|---|---|
| Python | [python.md](languages/python.md) |
| Rust | [rust.md](languages/rust.md) |


## Project Meta

Internal documents for codeOath itself.

| Document | Purpose |
|---|---|
| [decisions.md](meta/decisions.md) | Architecture decisions for codeOath itself |
| [style-guide.md](meta/style-guide.md) | Formatting rules for all docs |
| [todo.md](meta/todo.md) | Open tasks |
