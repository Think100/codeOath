# codeOath

Define your project in plain text. Your AI reads it, follows the rules, stops guessing.

You code with AI because it is fast and fun. But after a few weeks, things drift: files appear you did not ask for, decisions get forgotten, your AI starts doing its own thing.

codeOath starts with one text file where you write down what your project is, what it should not do, and what rules apply. Your AI reads it every session. As your project grows, you add structure step by step. The building blocks behind it are proven programming practices. You do not need to understand them to use them. Your AI does.

No framework, no install, no workflow to learn. Works with any AI tool today and will keep working when the tools change.


## Get Started

Read [start.md](docs/start.md). You will have your first project running in one vibe-coding session.

Or tell your AI right now:

> *"Create AGENTS.md with a project definition (what it is, what it is NOT, rules, structure), docs/todo.md, src/, tests/, and .gitignore. Show me the AGENTS.md before committing so I can review it."*

Already have a project that needs structure? [Start here](docs/resources/triggers.md#already-have-a-project).


## What AGENTS.md Looks Like

You write this file yourself. It is a plain text contract between you and your AI.

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

*Every AI tool has its own file for project instructions: Claude Code uses `CLAUDE.md`, Cursor uses `.cursorrules`, Copilot uses `.github/copilot-instructions.md`. codeOath calls it `AGENTS.md` because it works with any tool. Either rename it to match your tool, or add a one-liner to your tool's file: "Read AGENTS.md for project rules."*


## The Three Stages

Stage 1 is enough for most projects. Only add more structure when something starts going wrong.

| Stage | When | What | Guide |
|---|---|---|---|
| **1. Start** | Any project | AGENTS.md + todo.md | [start.md](docs/start.md) |
| **2. Grow** | Things get messy | Separate logic from infrastructure, document decisions | [grow.md](docs/grow.md) |
| **3. Enforce** | Rules keep getting broken | Automated checks, pick what you need | [enforce.md](docs/enforce.md) |

Not sure if you should move stage? Check the [triggers](docs/resources/triggers.md).


## See It in Action

One prompt, four outcomes. Each example was built by an AI that only read the matching guide.

> *"I want to track my expenses from the terminal. Use Python."*

| Stage | Result |
|---|---|
| [1: Start](examples/stage-1/expense-tracker/) | CLI, JSON storage, tests |
| [2a: Grow](examples/stage-2a/expense-tracker/) | domain/adapters split, SQLite, decisions.md |
| [2b: Grow](examples/stage-2b/expense-tracker/) | Ports, services layer, frozen dataclasses |
| [3: Enforce](examples/stage-3/expense-tracker/) | Import enforcement, pre-commit hooks, CI, ADRs |

[Full walkthrough and prompts](examples/README.md)


## All Guides

**Core:** [start.md](docs/start.md) · [grow.md](docs/grow.md) · [enforce.md](docs/enforce.md) · [AI Workflow](docs/ai-workflow.md)

**Resources:** [Triggers](docs/resources/triggers.md) · [Prompts](docs/resources/prompts.md) · [Testing](docs/resources/testing.md) · [Security](docs/resources/security.md) · [Performance](docs/resources/performance.md) · [Release Checklist](docs/resources/release-checklist.md)

**Architecture:** [Domain and Adapters](docs/resources/domain-and-adapters.md) · [Architecture Patterns](docs/resources/architecture-patterns.md) · [Philosophy](docs/resources/philosophy.md)

**Language Guides:** [Python](docs/languages/python.md) · [Language Conventions](docs/resources/language-conventions.md)


## FAQ

**Does this only work with Claude Code?**
No. Works with any AI tool. The examples use Claude Code file names; the principles are the same everywhere.

**Do I need programming experience?**
No. Stage 1 works for anyone who can use an AI coding tool. Your AI can teach you Git and everything else you need to get started.

**Is this a framework I need to install?**
No. Just conventions and file structures. Nothing to install.

**My project is already messy. Where do I start?**
Stage 1 add AGENTS.md and docs/todo.md. Then check the [triggers](docs/resources/triggers.md#already-have-a-project).

**How is this different from just writing a good README?**
AGENTS.md is structured to govern your project, not just describe it. The NOT field prevents scope creep. The rules tell your AI what to ask before acting. A README is for humans. AGENTS.md is for your AI and your future self.

**What if my AI ignores the rules?**
Check that AGENTS.md is in the project root and that your tool is configured to read it. If the AI still drifts, the rule is either too vague or too buried. Stage 3 adds automated enforcement.


---

Built for my own projects. Shared because others had the same problems.

[ROADMAP](ROADMAP.md) · [CHANGELOG](CHANGELOG.md) · [CC BY 4.0](LICENSE) -- Use it for anything, attribution required

https://github.com/Think100/CodeOath
