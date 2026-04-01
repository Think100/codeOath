> [README](../../README.md) > [Docs](../) > **Triggers**

# Migration Triggers

> **TL;DR** -- Add structure only when something hurts, not because a guide tells you to. This page lists common problems and what to do about them. Already have a project? Add AGENTS.md first, then reorganize one piece at a time. Start over from scratch only when the old technology is dead or the language changes.

## The Core Rule

**Never add structure preemptively.** If you are not feeling the pain, you do not need the cure. Structure that nobody maintains is worse than no structure at all.

When you do add structure: one step at a time. Add the layer separation, see if it helps, then decide if you need more. Do not jump from Stage 1 to Stage 3 in one session.


## Already Have a Project? (Refactoring)

If you already have a codebase and want to add codeOath structure, read the trigger tables below and find the symptoms that match your current pain. That tells you which stage to aim for. You do not have to start at Stage 1 if your project already has the problems of Stage 2 or 3.

1. Start with Stage 1 regardless: add `AGENTS.md` (with NOT field) and `docs/todo.md`. Low effort and helps immediately.
2. Do not reorganize code yet. First document what exists: what does each file do? What depends on what?
3. When you feel the pain (see triggers below), introduce Stage 2 concepts one at a time. Separate domain from adapters in the area that hurts most, not everywhere at once.
4. Use the Strangler Fig approach: build new structure next to the old, migrate piece by piece, then remove the old. This is the default for most projects.

### Migrating Step by Step

Ask your AI to help with the migration:

> "Read my AGENTS.md and understand the project. I want to migrate to a domain/adapters structure using the Strangler Fig approach. Do not rewrite everything at once. Pick the one file where business logic and infrastructure are most tangled. Extract the business logic into domain/ and the infrastructure code into adapters/. Create the port interface in domain/. Wire them together in main. Fix imports. Run the tests. Then stop and let me review before moving to the next file."

For the detailed step-by-step migration pattern (shim files, one-file-at-a-time commits, verification), see [How to Migrate Your Existing Code](../grow.md#how-to-migrate-your-existing-code).

### When Starting Fresh Makes More Sense

Sometimes migrating piece by piece costs more than it saves. Consider a clean rewrite when:

- **Language change:** You are moving from one language to another (e.g., C to Python). The old code is reference material, not a migration source.
- **Most of the code must change:** If you spend more time building bridges between old and new than on the actual restructuring, Strangler Fig is creating more overhead than it prevents.
- **Fundamental security flaw:** The architecture itself is compromised (e.g., secrets baked into the data model, no separation between user contexts). Patching cannot fix a broken foundation.
- **No tests and no understanding:** If nobody understands what the code does and there are no tests to verify behavior, migrating preserves bugs you cannot see.
- **Dead technology:** The framework or runtime itself is no longer maintained (e.g., AngularJS 1.x, Python 2, abandoned libraries). Migrating piece by piece inside a dying ecosystem means building bridges that will collapse anyway.

Even when rewriting: start with AGENTS.md. Define the project, the rules, and the structure before writing the first line. Keep the old codebase as read-only reference, do not delete it until the new version is verified. Do not try to replicate the old system 1:1; use the rewrite to fix the problems that caused the rewrite. A rewrite is not a license to build the system you always dreamed of. Fix what caused the rewrite, nothing more.




## From Nothing to [Stage 1](../start.md)

| When you notice...                       | Introduce...                          |
|------------------------------------------|---------------------------------------|
| You start a project and want AI to help  | `AGENTS.md` with project definition   |
| You forget what you planned to do next   | `docs/todo.md`                        |
| AI suggests features you do not want     | NOT field in `AGENTS.md`              |


## From Stage 1 to [Stage 2](../grow.md)

| When you notice...                                         | Introduce...                          |
|------------------------------------------------------------|---------------------------------------|
| AI creates files in wrong places or ignores your rules     | `domain/` and `adapters/` separation  |
| You forgot why you made a decision                         | `docs/decisions.md`                   |
| Database code mixed with business logic in the same file   | Split by layer (domain vs. adapter)   |
| You want to test your logic without a real database or API | Ports as interfaces in `domain/`      |
| AI keeps asking the same scope questions                   | Architecture rules in `AGENTS.md`     |
| Resolved items in todo.md are longer than open items       | `docs/todo_archive.md`               |
| You keep forgetting to check docs or dependencies          | Routines section in `todo.md`         |


## From Stage 2 to [Stage 3](../enforce.md)

| When you notice...                                         | Introduce...                                 |
|------------------------------------------------------------|----------------------------------------------|
| `AGENTS.md` is over 80 lines                              | `.claude/rules/` with path-specific loading  |
| Import rules violated (domain imports adapters)            | Import linter or architecture check          |
| Multiple people work on the code                           | Pre-commit hooks, branching strategy         |
| Use cases need own orchestration logic                     | `application/` layer                         |
| Need to distinguish incoming/outgoing adapters             | `adapters/in/` and `adapters/out/`           |
| AI reads files it should not                               | `.claude/settings.json` deny rules           |
| Security review needed before deployment                   | [Security checklist](security.md)            |
| Conventions drift silently                                 | Automated linting and formatting             |
| Project definition too long for `AGENTS.md`                | Extract to `docs/definition.md`              |
| Project runs as a service, bot, or scheduled job           | `docs/operations.md`                         |


## Beyond Stage 3

| When you notice...                                         | Consider...                                  |
|------------------------------------------------------------|----------------------------------------------|
| Parts need conflicting conventions                         | Splitting into separate projects             |
| Features block each other                                  | [Feature-sliced architecture](architecture-patterns.md) |
| Modules need hard boundaries                               | [Modular monolith](architecture-patterns.md)          |
| More than 10 architecture decisions per month              | Revisit the project definition               |
| The project definition feels wrong                         | Update it deliberately (Layer 1 change)      |
| `docs/todo.md` keeps growing | Scope is too big, prioritize ruthlessly |

