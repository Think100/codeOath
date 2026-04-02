> [README](../README.md) > **Start**

# Stage 1: Start

> **TL;DR** -- Create `AGENTS.md` (what your project is, what it is NOT, rules, structure) and `docs/todo.md` (tasks, open questions). Make sure your AI reads it every session. Commit before coding. Done.

Understand the basics in 10 minutes. Set up your first project in 30. Come back after four months and still know what you built.


## When You Are Here

You have an idea. Maybe a weekend project, maybe something that takes a few weeks. Up to about ten files. You want to start coding, not writing architecture documents.


## What You Need

- An AI coding tool (Claude Code, Cursor, Copilot, or similar)
- [Git](https://git-scm.com/) installed on your machine
- A text editor or IDE

New to any of these? Your AI can teach you. Ask it: *"Explain what Git is, why I need it, and help me install it."* That is the whole point of AI-assisted development: you do not need to know everything upfront.


## Set Up Your Project

Create these folders and files:

```text
myproject/
├── docs/
│   └── todo.md
├── src/
│   └── (your code here)
├── tests/
├── .gitignore
├── AGENTS.md
└── README.md
```

Your language might use a different folder layout (e.g., `<projectname>/` instead of `src/` in Python). A language-specific guide is available for [Python](languages/python.md).


## AGENTS.md: The One File That Matters

AGENTS.md is the only file you need to maintain in Stage 1. It tells your AI what the project is, what it is not, and what rules apply. Keep it short, around 80 lines or fewer.

Here is a complete example:

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
- Errors must be visible, never hide them silently
- New files: ask first (AI rule)
- New dependencies: ask first, explain why (AI rule)
- Commit after each completed task (AI rule)
- Prefix commits with your tool name: [claude], [cursor], [codex] (AI rule)
- When uncertain: ask, don't guess (AI rule)

## Structure
- Source: src/
- Tests: tests/
- Docs: docs/
- Tasks and open questions: docs/todo.md
```

You read it when you come back after months. Your AI reads it every session. Same file, two purposes.

**How your AI finds it:** Every tool has its own file name for project instructions. codeOath calls it `AGENTS.md` because it is tool-neutral. Either rename it to your tool's file name, or add a one-liner to your tool's file:

```markdown
# .github/copilot-instructions.md (Copilot)
Read AGENTS.md for project rules.
```

```markdown
# .cursorrules (Cursor)
Read AGENTS.md for project rules.
```

```markdown
# CLAUDE.md (Claude Code)
Read AGENTS.md for project rules.
```

Pick your tool, create the file, done. The AI reads it automatically from that point on.


### The NOT Field

This is the most important part. List at least three things your project will not do, and why. This kills scope creep (the project slowly growing beyond what it was supposed to be) before it starts. Every entry needs a reason. The reason prevents the same discussion from happening again.


## todo.md: One Place for Everything

Tasks, open questions, and resolved items in one file:

```markdown
# TODO

## Tasks
- [ ] Implement dry-run mode
- [ ] Add config file parsing

## Open Questions
- [ ] How should we handle files with no extension?
      Context: Currently skipped, but users might expect them sorted
      Priority: before first release

## Resolved
- [x] JSON or YAML for config? -> JSON (simpler, no indent issues)
```

If a question gets resolved, it moves to "Resolved" with the answer. No orphan questions, no lost decisions.


## Let Your AI Set It Up

You do not have to create all of this by hand. Tell your AI:

> "Create a new project called [name]. Create AGENTS.md with a project definition (what it is, what it is NOT, rules, structure), docs/todo.md with a Tasks and Open Questions section, src/, tests/, and .gitignore. Show me the AGENTS.md before committing so I can review it."

Review what it creates. The NOT field and the rules are the parts that matter most, so make sure they actually describe your project. Once you are happy with it, tell the AI to commit.

Here is what a successful setup looks like in the terminal:

```text
> Create a new project called csv2json with AGENTS.md, docs/todo.md, src/, tests/

Created AGENTS.md (42 lines)
Created docs/todo.md
Created src/
Created tests/
Created .gitignore

> Show me the AGENTS.md

# csv2json
CLI tool that converts CSV files to JSON.
## NOT
- Not a GUI (CLI is enough for one user)
- Not a web service (local only)
...

> Looks good, commit it

[main abc1234] init: project structure and rules
 4 files changed, 58 insertions(+)
```

If your output looks similar, you are set. The details will differ (your project name, your rules), but the structure is the same: AGENTS.md with a definition, NOT field, and rules.


## First Commit

Commit the structure before writing code. This gives you (and your AI) a clean baseline:

```bash
git add -A
git commit -m "init: project structure and rules"
```

**Keep committing.** A commit is a snapshot you can always go back to. Treat it like saving your game before a boss fight.

- Commit after each completed step, not at the end of the day
- One commit = one thing (not three bug fixes and a feature in one commit)
- Before a big change, commit what you have first (your safety net)
- Write what you did and why, not just "update" or "fix stuff"


## Coming Back After Months

You put the project aside. Now you are back. Read in this order:

1. `AGENTS.md` -- reminds you what the project is, what it is not, and what rules apply
2. `docs/todo.md` -- shows what was planned, what questions were open, what was resolved

That is the point of this structure: the files that steered your AI also bring you back up to speed.


## One Rule About Security

No passwords, API keys, or tokens in your code. Ever. Put them in environment variables. If you accidentally commit a secret, it is in your git history forever. Change the password or rotate the credential immediately.

That is the one thing you must get right from day one. For everything else, see [security.md](resources/security.md) when you are ready.


**Want to get more out of your AI?** Tips for multi-perspective reviews, session habits, and reusable agents: [ai-workflow.md](ai-workflow.md).


## When This Setup Is No Longer Enough

You do not need to read further right now. Build your project. Come back when you notice one of these:

- Your AI puts files in the wrong places or mixes database code with business logic
- You cannot remember why you made a decision two weeks ago

When that happens: [Stage 2](grow.md). For the full list of signs: [triggers](resources/triggers.md).
