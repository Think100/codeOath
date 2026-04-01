> [README](../README.md) > **Enforce**

# Stage 3: Enforce

> **TL;DR** -- You keep running into the same problem, so you automate the solution. This is a menu: pick the one item that solves your current pain, ignore the rest.

If you are not sure you need this, check [triggers.md](resources/triggers.md). If Stage 2 still works fine, stay there.


## The Same Rule Keeps Getting Broken

### Import Enforcement

The rule "domain must never import from adapters" was a convention. Your AI or you can ignore conventions. Import enforcement turns it into an automated check that fails if violated.

One of codeOath's core philosophies: not a rule that someone might forget, but a check that physically prevents the violation.

The specific tool depends on your language. Some have dedicated linters (import-linter for Python, eslint-plugin-boundaries for JavaScript). Some enforce boundaries through their compiler (Rust's module visibility, Go's `internal/` packages). Others have test-based tools (Java's ArchUnit, .NET's NetArchTest). The principle is the same: define which modules may import from which, and fail if violated.

> "Read my AGENTS.md and the architecture rules. Set up import enforcement for this project. The rule is: domain/ must never import from adapters/ or application/. adapters/ may import from domain/. Fail the build if violated. Use the standard tool for my language. If no dedicated tool exists and the compiler does not enforce it, write a script that checks for violations."

If your AI generates a custom script instead of using an established tool: **review it before adding it as a pre-commit hook.** A script that parses imports with regex is not as reliable as a tool that understands the language. Test it against known violations and known valid code before you trust it.

### Pre-Commit Hooks

You keep finding problems after they are already committed. Pre-commit hooks are scripts that run automatically every time you type `git commit`. If a check fails, the commit is blocked. They catch problems before they enter your git history:

- **Linter** (catches code style issues and common mistakes)
- **Formatter** (keeps formatting consistent)
- **Import checker** (enforces the architecture boundaries from above)
- **Secret scanner** (catches passwords and API keys before they end up in git)

Pre-commit hooks are cheap: they run locally in seconds, catch problems instantly, and do not consume AI context or API calls. The AI does not need to be involved in formatting or linting; the tools handle it automatically.

> "Set up pre-commit hooks for this project: linter, formatter, import checker, and secret scanner. Make sure they run automatically before every git commit."

### Testing Strategy

You are not sure which parts of your code are actually tested. Define what gets tested where so nothing falls through the cracks. For what each type of test does, see [testing.md](resources/testing.md).

> "Read my AGENTS.md and review the test coverage. Create a test plan: which domain logic needs unit tests? Which adapters need their own tests? Add basic security tests. Set up the test suite to run in CI."


## The Structure Is Not Enough Anymore

Your domain/adapters split works, but the project is growing and you need more granularity.

### Application Layer

Your use cases mix orchestration with business logic. The solution: add an application layer between domain and adapters. Think of it as the manager: "load the invoice, apply the discount, save the result, send the email."

```text
src/
  domain/             pure logic, ports
  application/        use cases, orchestration (NEW)
  adapters/
    in/               incoming: CLI, HTTP, bot, scheduler (NEW)
    out/              outgoing: DB, email, APIs, filesystem (NEW)
  main.*
```

Import direction: `adapters/ --> application/ --> domain/`. Domain imports nobody.

Only add this when the flat domain/adapters split is no longer enough.

> "Read my AGENTS.md. My use cases mix orchestration with business logic. Introduce an application/ layer: extract use case orchestration from domain/ into application/use_cases.*. Domain should only contain pure logic. Update the import rules accordingly."

### Architecture Decision Records (ADR)

Your decisions.md is getting long and decisions need more context than one line. Split into individual files under `docs/adr/`. Each file contains: Date, Status, Context (why), Decision (what), Consequences (what changes).

> "Migrate my docs/decisions.md to individual ADR files under docs/adr/. Create 0001-template.md as a reusable template."

### AGENTS.md Is Too Long

Two solutions, use one or both:

**Extract the project definition** to `docs/definition.md`. AGENTS.md references it: "Read `docs/definition.md` for scope questions."

**Extract naming conventions** to `docs/conventions.md` if your project has 50+ files and naming rules that no longer fit in AGENTS.md (file naming patterns, URL schemes, database column conventions). AGENTS.md references it: "Read `docs/conventions.md` for naming rules." This keeps AGENTS.md focused on architecture and behavior.

**Split rules by path.** Rules load only when your AI touches specific paths:

```text
.claude/
  rules/
    domain.md          loaded only when touching domain/ files
    adapters.md        loaded only when touching adapters/ files
    tests.md           loaded only when touching tests/ files
```

> "My AGENTS.md is over 80 lines. Split the architecture rules into .claude/rules/ files: one for domain/, one for adapters/, one for tests/. Keep AGENTS.md short."

Here is what a Stage 3 AGENTS.md looks like after splitting out the details:

```markdown
# myproject

CLI tool that converts CSV files to JSON.

## NOT
- Not a GUI (CLI is enough for one user)
- Not a web service (local only, no server complexity)
- Not handling Excel files (out of scope, CSV only)

## Rules
- Python 3.14+
- No secrets in code or version control
- New files: ask first (AI rule)
- Prefix commits with your tool name: [claude], [cursor], [codex] (AI rule)
- Never amend or force-push without asking (AI rule)
- Never delete files without confirmation (AI rule)
- Check existing patterns before introducing new ones (AI rule)
- When uncertain: ask, don't guess (AI rule)

## Language Conventions
| What | Language | Why |
|---|---|---|
| Code (variables, functions) | English | Universal, libraries expect it |
| Code comments | English | Same language as the code |
| Commit messages | English | Git history searchable |
| AGENTS.md, docs/ | Your language | Your thinking tool, your language |
| README.md | Depends | Open-source: English. Private: yours |

## Architecture
domain/       core logic, no external imports
application/  use cases, orchestration
adapters/     database, API, files, UI
main          connects everything

Rule: domain imports nobody. application imports domain. adapters import both.

For detailed rules per layer: see .claude/rules/

## Structure
- Source: src/ (domain/, application/, adapters/, main.*)
- Tests: tests/
- Docs: docs/
- Decisions: docs/adr/
- Scope: docs/definition.md
- Operations: docs/operations.md

## Navigation
For database work: read src/adapters/db/ and docs/adr/
For business logic: read src/domain/
For test changes: read tests/ and .claude/rules/tests.md
```


## Multiple Contributors Are Stepping on Each Other

### Commit Prefixes

You cannot tell who changed what. Prefix every AI-generated commit with the agent's name:

```text
[claude] fix: input validation on upload endpoint
[cursor] add: user profile page
(no prefix = human)
```

### Read-Only Agents for Audits

Your AI agents keep making unintended changes during reviews. Solution: give audit agents read-only access. A test runner that can only execute tests. A contract checker that reads code and docs but cannot change anything. An agent that can only read cannot accidentally break things.

### Minimal-Scope Agents

A general-purpose agent that "checks everything" will miss things and waste context. Instead, give each audit agent one job and the smallest possible scope:

- **Import auditor:** reads `src/` and the import rules, reports violations. No write access, no test files.
- **Security scanner:** reads `src/` and `docs/security.md`, flags issues. No fixing, just reporting.
- **Test coverage checker:** reads `tests/` and `src/`, reports untested paths. No code generation.

The principle: one agent, one question, minimal file access. A focused agent with 20 files of context produces better results than a broad agent with 200.

### Navigation Hints

Your AI scans the entire repo for every task. Help it find the right files faster:

```markdown
## Navigation

For database work: read src/adapters/db/ and docs/decisions.md
For business logic: read src/domain/

### Large files (read with offset, not in full)
- src/adapters/db/queries.py (600+ lines): Job queries 1-380, Outbox 384-450
```

### Branching Strategy

People push directly to main and break things. Protect main:

- `main` is protected (no direct pushes)
- Features on branches, changes through pull requests
- AI-generated commits prefixed (e.g., `[claude]`)

> "Set up branch protection for main: require pull requests, require at least one approval, require all CI checks to pass before merging."

### CI/CD Pipeline

CI/CD (Continuous Integration / Continuous Deployment) means a server automatically runs checks on your code every time you push. Pre-commit hooks can be skipped (`--no-verify`). A CI/CD pipeline runs the same checks on a server where nobody can bypass them.

At minimum: linter, formatter, import checker, test suite, secret scan.

> "Set up a CI pipeline that runs on every push: linter, formatter, import enforcement, secret scanner, and the full test suite. Block merges to main if any check fails."

### Operations Documentation

Your project runs as a service but nobody knows how to restart it. Create `docs/operations.md` covering: Startup (prerequisites, env vars, commands), Monitoring (logs, health checks), Backup (what, how often, restore), Retention (what grows, cleanup policy), Troubleshooting (common problems).

**Data retention matters.** Without a cleanup policy, storage grows silently until the disk is full. A simple rule: "logs: 30 days, completed jobs: 90 days, temp files: 7 days."

**Health checks save debugging time.** A `/health` endpoint that returns "OK" answers "is it running?" in one second instead of ten minutes.

> "Read my AGENTS.md. Create docs/operations.md with the sections that apply to this project. Skip sections that do not apply."


## Cross-Cutting Concerns

Security and performance apply from day one, not just at Stage 3: [Security](resources/security.md), [Performance](resources/performance.md).


## Beyond Stage 3

If your project has 20+ modules with conflicting conventions or features blocking each other, you may need a different architecture style: [architecture-patterns.md](resources/architecture-patterns.md) covers feature-sliced, modular monolith, or splitting into separate projects.

The codeOath principles still apply at that scale. "Define before you build", "lower layers never violate upper layers", "maintenance must be cheap": these do not expire. What changes is the mechanism: instead of one AGENTS.md you might have one per module, instead of one decisions.md you have an ADR directory, instead of folder-based separation you have package-based boundaries. The thinking stays the same. The tools grow with the project.
