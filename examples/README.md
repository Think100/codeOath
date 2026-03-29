# Examples

Expense tracker CLI built stage by stage. Each folder is a complete, runnable project that shows one stage of codeOath.

The core prompt was always the same: "I want to track my expenses from the terminal." For each stage, we pointed the AI at a different guide (start.md, grow.md, enforce.md) so the results show clear progression. The exact prompts are below. No manual constraints on structure or file count. What you see is what the AI produced.


## At a Glance

| | Stage 1 | Stage 2a | Stage 2b | Stage 3 |
|---|---|---|---|---|
| **Guide read** | start.md | grow.md (to break) | grow.md (full) | all three |
| **Files** | 4 .py | 5 .py | 6 .py | 8 .py + config |
| **Structure** | flat package | domain/ + adapters/ | + ports, services | + application/, inbound/outbound |
| **Storage** | JSON | SQLite | JSON | SQLite |
| **Tests** | yes (AI added) | yes | yes | yes (per layer) |
| **AGENTS.md** | basic | + Architecture section | + per-file docs | + Navigation hints, German |
| **decisions.md** | no | yes | yes | ADRs with numbers |
| **Enforcement** | none | none | none | pre-commit, import-linter, CI |
| **Dependencies** | stdlib only | stdlib only | stdlib only | click, import-linter |


## Stage 1

Prompt given to Claude Sonnet:

> I want to track my expenses from the terminal. Simple Python CLI, nothing fancy. Read docs/start.md and follow that structure. Build it in examples/stage-1/. No other steps.

The AI built a working CLI with tests and a package structure on its own. That is fine. codeOath does not restrict what your AI builds. It gives your AI context so it builds the right thing.


## Stage 2a

Prompt given to Claude Sonnet:

> I want to track my expenses from the terminal. Python CLI. Read docs/grow.md up to "You can stop here" and follow that structure. Build it in examples/stage-2a/. No other steps.

The AI split the code into `domain/` (core logic, no external imports) and `adapters/` (SQLite, CLI), wired them in `main.py`, and documented decisions in `docs/decisions.md`. 16 tests pass.


## Stage 2b

Prompt given to Claude Sonnet:

> I want to track my expenses from the terminal. Python CLI. Read docs/grow.md completely and follow that structure. Build it in examples/stage-2b/. No other steps.

The AI read past "You can stop here" and built the full Stage 2: domain/adapters split, `typing.Protocol` ports, a separate `services.py` for pure logic, and frozen dataclasses.


## Stage 3

Prompt given to Claude Sonnet:

> I want to track my expenses from the terminal. Python CLI. Read docs/start.md, docs/grow.md, and docs/enforce.md. Follow all three stages. Build it in examples/stage-3/. No other steps.

The AI built the full stack: domain/application/adapters layers, `.claude/rules/` with per-layer constraints, pre-commit hooks, CI pipeline, import-linter enforcement, and formal ADRs. It also adopted the repo's language conventions (German AGENTS.md, English code).


## What We Learned

**The AI builds more than you ask for.** Stage 1 was supposed to be "simple, nothing fancy." The AI added tests, a package structure, and a pyproject.toml on its own. Stage 2a was supposed to stop before Ports, but the AI added them anyway. This is not a bug. AI models in 2026 already produce structured code by default.

**Same prompt, different results.** Stage 2a chose SQLite, Stage 2b chose JSON. Stage 2a uses Decimal for money, Stage 2b uses float. Neither was specified. The AI makes its own design decisions, and they vary between runs.

**The guide shapes the architecture, not the details.** What changes clearly between stages is the structure: flat code (Stage 1), domain/adapters split (Stage 2), full enforcement with CI and rules (Stage 3). The implementation details (which database, which types) are up to the AI.

**Constraining the AI is harder than guiding it.** We tried limiting Stage 1 with "nothing fancy" and Stage 2a with "up to You can stop here." The AI read the docs and made its own judgment. codeOath works best as a guide, not a constraint.
