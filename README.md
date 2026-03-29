# codeOath

**Your AI project will not fall apart. One file, a few rules, done.**

A project guide for AI-assisted development.

You code with AI. It works fast. After two weeks, nobody understands the codebase anymore. Your AI creates files you did not ask for and rewrites things you did not want touched. You come back after a break and neither of you remembers what was decided.

codeOath fixes all of that. Here is what that one file looks like:

```markdown
# myproject

CLI tool that converts CSV files to JSON.

## NOT
- Not a GUI (CLI is enough for one user)
- Not a web service (local only, no server complexity)
- Not handling Excel files (out of scope, CSV only)

## Rules
- Python 3.14+
- Code and comments in English
- Never overwrite input files
- No secrets in code or version control
- New files: ask first (AI rule)
- New dependencies: ask first (AI rule)
- Commit after each completed task (AI rule)
- Prefix commits with your tool name: [claude], [cursor], [codex] (AI rule)
- When uncertain: ask, don't guess (AI rule)

## Structure
- Source: src/
- Tests: tests/
- Docs: docs/
- Tasks and open questions: docs/todo.md
```

That is your `AGENTS.md`. You read it when you come back after months. Your AI reads it at the start of each session, if you tell it to (or if your tool loads it automatically).

*Every AI tool has its own file for project instructions: Claude Code uses `CLAUDE.md`, Cursor uses `.cursorrules`, Copilot uses `.github/copilot-instructions.md`. codeOath calls it `AGENTS.md` because it works with any tool. Either rename it to match your tool, or add a one-liner to your tool's file: "Read AGENTS.md for project rules."*


## Get Started

One document to start: [start.md](docs/start.md). Everything else is optional until you need it. Ten minutes to understand, thirty to set up.

Or tell your AI right now:

> *"Create AGENTS.md with a project definition (what it is, what it is NOT, rules, structure), docs/todo.md, src/, tests/, and .gitignore. Show me the AGENTS.md before committing so I can review it."*

Already have a project that needs structure? [Start here](docs/resources/triggers.md#already-have-a-project).


## See It in Action

Same project, four prompts, four levels of structure. Each built from scratch by an AI that only read the matching guide.

> *" I want to track my expenses from the terminal use Python"*

| Stage | Project | What the AI built |
|---|---|---|
| **1** | [expense-tracker](examples/stage-1/expense-tracker/) | Python CLI, JSON storage, tests, package structure |
| **2a** | [expense-tracker](examples/stage-2a/expense-tracker/) | domain/adapters split, SQLite, decisions.md |
| **2b** | [expense-tracker](examples/stage-2b/expense-tracker/) | Ports (Protocol), services layer, frozen dataclasses |
| **3** | [expense-tracker](examples/stage-3/expense-tracker/) | Layer enforcement, pre-commit hooks, CI, ADRs, path-specific rules |

[Full walkthrough and prompts used](examples/README.md)


## When You Need More

Most projects do fine at Stage 1. When yours outgrows it, move when you feel the pain, not on a schedule.

| Stage | When | What | Guide |
|---|---|---|---|
| **1. Start** | New project | AGENTS.md + todo.md | [start.md](docs/start.md) |
| **2. Grow** | Things get messy | Separate logic from infrastructure, document decisions | [grow.md](docs/grow.md) |
| **3. Enforce** | Rules keep getting broken | Automated checks, pick what you need | [enforce.md](docs/enforce.md) |

Not sure if you should move? Check the [triggers](docs/resources/triggers.md).

Stage 2's first addition is `decisions.md`: when your AI asks "should we use JSON or YAML?", the answer is already written down.


## Reference

Look things up when you need them. Not required reading.

**Practical:**

| Guide | What it covers |
|---|---|
| [AI Workflow](docs/ai-workflow.md) | Session habits, multi-perspective reviews, reusable agents |
| [Language Conventions](docs/resources/language-conventions.md) | Which language to use where (code, comments, docs, commits) |
| [Prompt Cheatsheet](docs/resources/prompts.md) | Every copy-paste prompt in one place |
| [Triggers](docs/resources/triggers.md) | When to move from one stage to the next |

**Background (for when you want to understand why):**

| Guide | What it covers |
|---|---|
| [Testing](docs/resources/testing.md) | AI writes tests, you review, domain-first testing |
| [Security](docs/resources/security.md) | Input validation, secrets, auth, common vulnerabilities |
| [Performance](docs/resources/performance.md) | Database, caching, timeouts, crash recovery |
| [Ports and Adapters](docs/resources/ports-and-adapters.md) | The architecture pattern behind Stage 2 |
| [Alternatives](docs/resources/alternatives.md) | Feature-sliced, modular monolith, vertical slices |
| [Philosophy](docs/resources/philosophy.md) | The principles behind codeOath |
| [Python guide](docs/languages/python.md) | How codeOath concepts translate to Python |


## FAQ

**Does this only work with Claude Code?**
No. Works with any AI tool. The examples use Claude Code file names; the principles are the same everywhere.

**Do I need programming experience?**
No. Stage 1 works for anyone who can use an AI coding tool. Your AI can teach you Git and everything else you need to get started.

**Is this a framework I need to install?**
No. Just conventions and file structures. Nothing to install.

**My project is already messy. Where do I start?**
Stage 1 anyway. Add AGENTS.md and docs/todo.md, costs nothing. Then check the [triggers](docs/resources/triggers.md#already-have-a-project).

**How is this different from just writing a good README?**
AGENTS.md is structured to govern your project, not just describe it. The NOT field prevents scope creep. The rules tell your AI what to ask before acting. A README is for humans browsing GitHub; AGENTS.md is for your AI and your future self.

**What if my AI ignores the rules?**
Check that AGENTS.md is in the project root and that your tool is configured to read it. If the AI still drifts, the rule is either too vague or too buried. Stage 3 adds automated enforcement that catches violations before they are committed.


---

Built for my own projects. Shared because others had the same problems.

[ROADMAP](ROADMAP.md) | [CHANGELOG](CHANGELOG.md) | [CC BY 4.0](LICENSE) -- Use it for anything, attribution required

https://github.com/Think100/CodeOath
