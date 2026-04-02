> [README](../README.md) > **Grow**

# Stage 2: Grow

> **TL;DR** -- (1) Split your code: `domain/` for logic, `adapters/` for database/API/files, `main` to connect them. (2) Write down decisions in `docs/decisions.md`. That covers 80% of the chaos. Concepts 3 (ports) and 4 (testing) are optional until you need them.

Understand the concepts in 20 minutes. Migrate your project in an afternoon.

Your project has more than ten files. Your AI is putting things in the wrong places. Database code and business logic are mixing. You forgot why you made a decision. Things are getting messy. If that is not you yet, check [triggers.md](resources/triggers.md) or stay at [Stage 1](start.md).


## What Changes

Four new concepts. That is all. But do them in order, not all at once.

**Start here** (you can do this today):

1. **Separate your logic** from the outside world (database, API, files)
2. **Document your decisions** so they are not forgotten

**Add later** (when the folder split alone is no longer enough):

3. **Define what your logic needs** using contracts (ports and adapters)
4. **Start testing** your logic independently

Concepts 1 and 2 are straightforward. Concepts 3 and 4 are more advanced, but this guide explains them in plain language. Your AI can help you implement all of them.


### 1. Separate Your Logic from the Outside World

The idea is simple: split your code so that your core logic does not depend on the outside world.

(If you want to sound smart: this pattern is called *Hexagonal Architecture*, also known as *Ports and Adapters*. It is a well-established approach used in professional software engineering. codeOath uses it because it fits well with AI-assisted development. There are [other approaches](resources/architecture-patterns.md) if you are curious.)

**domain/** (your logic) is where the core of your project lives. The rules, the calculations, the things that make your project do what it does. This code does not know about databases, APIs, or files. It just knows the rules.

**adapters/** (the outside world) is everything that talks to external systems. Database, HTTP, file system, UI, bot. If you swap your database from SQLite to PostgreSQL, only adapter code changes. Your logic stays the same.

**main** (the glue) is the one place where you connect the two. It creates the database connection, creates the logic, and hooks them together. Nothing else does this.

**config/** (settings) is where database paths, API endpoints, timeouts, and feature flags live. One place for all settings, not scattered across your code. Your domain code never reads config files directly; it receives settings as parameters from main.

Your project now looks like this:

```text
myproject/
├── config/                      <- NEW: settings, environment defaults
│   └── settings.*
├── docs/
│   ├── todo.md
│   └── decisions.md             <- NEW: why you made decisions
├── src/
│   ├── domain/                  <- NEW: your logic, no external dependencies
│   │   └── models.*
│   ├── adapters/                <- NEW: database, API, files, UI
│   │   ├── db.*
│   │   ├── api.*
│   │   └── cli.*
│   └── main.*                   <- connects domain and adapters
├── tests/
│   ├── test_domain.*
│   └── test_adapters.*
├── .gitignore
├── AGENTS.md                    <- updated with architecture + decisions
└── README.md
```

Your language might use a different folder layout. A language-specific guide is available for [Python](languages/python.md).

**The one rule:** adapters may use domain code. Domain must never use adapter code. Always in this direction:

```text
adapters/  -->  domain/
domain/    -->  NOBODY (no external imports)
```

**What about logging?** Your domain code does not know whether it runs in a web server, a CLI tool, or a test. So it should not decide where to log. Let the adapter handle logging. Domain code returns results or raises errors.


### 2. Document Your Decisions

Without a record of your decisions, you (and your AI) will revisit the same questions over and over. "Should we use JSON or YAML?" gets decided, forgotten, and debated again two weeks later. That wastes time and creates inconsistency.

Create `docs/decisions.md`. One file, simple format:

```markdown
# Decisions

## 2026-03-26: JSON instead of YAML for configuration
**Status:** active
JSON. Simpler to parse, no indentation issues, built-in support in every language.

## 2026-03-25: SQLite instead of PostgreSQL
**Status:** active
SQLite. Single user, local data, no server needed. Revisit if we need concurrent access.

## 2026-03-24: Add caching layer
**Status:** planned
Not implemented yet. Will add when response times become a problem.

## 2026-03-20: Markdown for all docs
**Status:** replaced by 2026-03-26 decision
Was plain text. Switched to Markdown for better readability.
```

Date, decision, status, reason. Status is one of: **active** (still applies), **planned** (decided but not yet implemented), **replaced** (a newer decision supersedes it), or **dropped** (we tried it, it did not work). When your future self (or your AI) asks "why did we do it this way?", the answer is here. Stage 3 builds on this when one file is no longer enough.

As your project grows, add a **Known Risks** section at the bottom of decisions.md. These are things you know about but choose not to fix right now. Documenting them prevents the same discussion from happening again and helps your future self (or a new contributor) understand what to watch for.

```markdown
## Known Risks

| Risk | Mitigation |
|---|---|
| SQLite does not handle concurrent writes well | Single worker, revisit if we need multiple |
| API rate limit could block long jobs | Exponential backoff, manual retry if needed |
| Config file is not validated on startup | Add schema validation when config grows |
```

One line per risk. Risk plus mitigation. If the mitigation is "we accept this for now", write that.


### Your Task List Grows Up

In Stage 1, `docs/todo.md` was a flat list. As the project lives longer, two things happen: completed items pile up, and you start needing recurring checks.

**Routines** are recurring tasks with no fixed due date. Add a `Routines` section to your todo.md:

```markdown
## Routines

- [ ] Check docs match current code (last: 2026-04-10, every: 2 weeks)
- [ ] Update dependencies, check for known vulnerabilities (last: 2026-04-01, every: month)
- [ ] Security scan: no secrets in code, input validation at boundaries (last: 2026-03-25, every: month)
```

Each routine has a `last:` date and an `every:` frequency so you know when it is due. Start with documentation accuracy and dependency audit. Add more when you feel the need.

Suggested frequencies as a starting point:

| Routine | Frequency | Why |
|---|---|---|
| Docs accuracy check | Every 2 weeks | Docs drift fast during active development |
| Dependency audit | Monthly | CVEs are published continuously. See [dependency evaluation](resources/dependency-evaluation.md) |
| Security scan | Monthly | Catches secrets or validation gaps before they accumulate |
| AI code review | Monthly | Catches hidden errors and fake safety in AI-generated code. See [ai-code-review](resources/ai-code-review.md) |
| Architecture check | Monthly | Detects boundary violations early |
| Performance spot check | Quarterly | Only relevant once real data flows |

These are defaults, not rules. A project under heavy development might check docs weekly. A stable project might audit dependencies quarterly. Adjust to your pace.

> "Read my AGENTS.md and docs/todo.md. Pick the routine with the oldest `last:` date. Run that check now: read the relevant files, verify the current state, report any issues, and update the `last:` date."

**Archive:** when the Resolved section in todo.md gets longer than the open items, move completed entries to `docs/todo_archive.md`. Same format, different file. Keeps todo.md focused.


---

**You can stop here. Most projects do.** Concepts 1 and 2 (folder split + decisions file) solve 80% of the chaos. If your project feels organized and your AI puts things in the right places, you are done with Stage 2. Do not add more structure just because it exists.

---


## When Folders Are Not Enough

The next two concepts solve a specific frustration: your AI keeps importing database code inside `domain/`, or you want to test your logic but cannot because it is wired to a real database. If neither of these bothers you today, come back when they do.


### 3. Define What Your Logic Needs

Your domain code needs data from the outside (a database, a file, an API) but it should not know *how* that data is fetched.

**Think of it like a restaurant.** The chef (your domain logic) says: "I need ingredients." The chef does not care whether the ingredients come from a local farm, a supermarket, or a warehouse. The chef just describes what is needed. The supplier (your adapter) goes and gets it.

In code, this means: instead of your logic directly talking to the database, you write a description of what it needs. This description is called a **port**. The code that actually talks to the database is the **adapter**. Your logic only knows the port, never the adapter.

In practice, you create three things:

1. **The description** (port): a file in `domain/` that says "I need something that can save an invoice and find an invoice by ID." It does not say how. Just what.

2. **The supplier** (adapter): a file in `adapters/` that actually talks to the database. It fulfills the description: "Here is how I save and find invoices using SQL."

3. **The wiring** (main): one line in `main` that says "Use this specific supplier to fulfill that description."

Your domain code only ever sees the description, never the supplier. If you replace SQLite with PostgreSQL tomorrow, you write a new supplier. The domain code does not change.

For the concrete code syntax, see [languages/python.md](languages/python.md) or [domain-and-adapters.md](resources/domain-and-adapters.md) for the full pattern with examples.

**Why bother?** Three reasons:

1. You can swap the database without touching your logic. SQLite today, PostgreSQL tomorrow, only the adapter changes.
2. You can test your logic without a real database. Just create a test adapter that stores everything in memory.
3. Your AI sees clear boundaries: in `domain/`, no database imports allowed.

There are two kinds of ports: ones where the outside world calls your logic (e.g., a button click triggers a calculation), and ones where your logic needs something from outside (e.g., saving data). The example above shows the second kind. For both kinds explained in detail, see [domain-and-adapters.md](resources/domain-and-adapters.md).


### 4. Start Testing

Because you separated your logic from the outside world, testing becomes much easier. Your domain code has no external dependencies, so tests are fast and simple.

**Without separation** (everything tangled): to test whether a discount is calculated correctly, you need a real database with test data, a running server, and cleanup afterward. The test is slow, brittle, and breaks when the database schema changes.

**With separation** (domain isolated): the discount logic takes an order and returns a number. No database, no server, no cleanup. The test runs in milliseconds:

```text
test "10% discount on orders over 100":
    order = Order(items=[Item(price=120)])
    result = apply_discount(order)
    assert result.total == 108
```

Back to the restaurant analogy: you are testing the chef's recipe, not the delivery truck. The recipe works the same whether ingredients come from a farm or a supermarket.

**What to test where:**

- **Domain tests:** pure logic, fast, no setup. "Does the calculation return the right result?"
- **Adapter tests:** real external calls. "Does the database adapter actually save and load correctly?"
- **Security tests:** boundary checks. "Does the system reject bad input?"

Ask your AI to get you started:

> "Read my AGENTS.md and look at the code in domain/ and adapters/. Create tests under tests/: unit tests for all domain logic, basic security tests (reject bad input, no secrets in responses or logs), and set up language-specific checks (type checking, linting, formatting) for this project."

This prompt sets up three different things (unit tests, security tests, static analysis). For what each one does and why, see [testing.md](resources/testing.md).


## How to Migrate Your Existing Code

Before you let your AI reorganize, update your project first:

**Step 1: Update your AGENTS.md.** Add the architecture section so your AI knows the new rules. Here is a complete Stage 2 example:

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
- Prefix commits with your tool name: [claude], [cursor], [codex] (AI rule)
- When uncertain: ask, don't guess (AI rule)

## Architecture
domain/    core logic, no external imports
adapters/  database, API, files, UI
main       connects domain and adapters

Rule: adapters may use domain. Domain must never use adapters.

## Structure
- Source: src/ (domain/, adapters/, main.*)
- Tests: tests/
- Docs: docs/
- Decisions: docs/decisions.md
```


**Step 2: Create the folders.** Create `src/domain/`, `src/adapters/`, `docs/decisions.md`, and `tests/` if they do not exist yet.

**Step 3: Let your AI migrate the code.** The safe way to migrate is one file at a time, with a commit between each move. Why? Because if something breaks, you can revert just that one step instead of untangling a massive change.

The pattern:

1. Copy the file to its new location (e.g., `utils.py` to `domain/utils.py`)
2. At the old location, create a shim (a small forwarding file that re-exports everything from the new location). This means nothing breaks yet because all imports still work.
3. Update imports across the project to point to the new location
4. Remove the shim once no imports use the old path
5. Commit after each step

Give your AI this prompt:

> "Read my AGENTS.md to understand the project. Migrate the code in src/ into domain/ and adapters/ following the architecture rules. Move one file at a time using this pattern: (1) copy file to new location, (2) leave a re-export shim at the old location so nothing breaks, (3) update all imports to the new path, (4) remove the shim, (5) commit. Files with no external dependencies go into domain/. Everything else goes into adapters/. Create a main.* that connects them. Stop after each file and let me review before moving to the next."

**Step 4: Verify the result.**

> "Review the project structure. Check that domain/ has no imports from adapters/ and that no adapter is directly created inside domain/. Check that all external dependencies are in adapters/. Check that main.* is the only file that connects the two. Check that no re-export shims remain. Run the tests and make sure they pass."


## When This Setup Is No Longer Enough

Two signs that you need [Stage 3](enforce.md):

1. Your AI keeps violating the import rule (domain imports adapters), and you have no way to catch it automatically.
2. Multiple people work on the code and conventions start to drift.

For the full list of signs, see [triggers.md](resources/triggers.md). Curious why these rules exist? [philosophy.md](resources/philosophy.md#ai-rules-and-engineering-rules) explains the thinking.

**Language mixing?** If your AI mixes English and your native language, see [language-conventions.md](resources/language-conventions.md).
