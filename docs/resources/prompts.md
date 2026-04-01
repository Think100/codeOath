> [README](../../README.md) > [Docs](../) > **Prompt Cheatsheet**

# Prompt Cheatsheet

> **TL;DR** -- Copy-paste prompts for every stage: Stage 1 (project setup), Stage 2 (migration, testing, maintenance), Stage 3 (enforcement, CI/CD). Plus security audits, performance reviews, workflow prompts, and architecture alternatives. No explanations here, see linked source docs for context.

Every copy-paste prompt from codeOath in one place. No explanations. Copy what you need.

For context on when and why to use each prompt, see the linked source document.


## Stage 1: Start

**Set up a new project** ([start.md](../start.md))

> "Create a new project called [name]. Create AGENTS.md with a project definition (what it is, what it is NOT, rules, structure), docs/todo.md with a Tasks and Open Questions section, src/, tests/, and .gitignore. Show me the AGENTS.md before committing so I can review it."


## Stage 2: Grow

**Migrate existing code into domain/adapters** ([grow.md](../grow.md))

> "Read my AGENTS.md to understand the project. Migrate the code in src/ into domain/ and adapters/ following the architecture rules. Move one file at a time using this pattern: (1) copy file to new location, (2) leave a re-export shim at the old location so nothing breaks, (3) update all imports to the new path, (4) remove the shim, (5) commit. Files with no external dependencies go into domain/. Everything else goes into adapters/. Create a main.* that connects them. Stop after each file and let me review before moving to the next."

**Verify architecture after migration** ([grow.md](../grow.md))

> "Review the project structure. Check that domain/ has no imports from adapters/ and that no adapter is directly created inside domain/. Check that all external dependencies are in adapters/. Check that main.* is the only file that connects the two. Check that no re-export shims remain. Run the tests and make sure they pass."

**Create tests** ([grow.md](../grow.md))

> "Read my AGENTS.md and look at the code in domain/ and adapters/. Create tests under tests/: unit tests for all domain logic, basic security tests (reject bad input, no secrets in responses or logs), and set up language-specific checks (type checking, linting, formatting) for this project."

**Set up maintenance routines** ([grow.md](../grow.md))

> "Read my AGENTS.md and docs/todo.md. Add a Routines section to todo.md with recurring maintenance tasks that fit this project. For each routine, describe what to check and add a `last:` date placeholder. Include at minimum: documentation accuracy check and dependency audit. Only add routines that make sense for this specific project."

**Run a routine check** ([grow.md](../grow.md))

> "Read my AGENTS.md and docs/todo.md. Pick the routine with the oldest `last:` date. Run that check now: read the relevant files, verify the current state, report any issues, and update the `last:` date. If you find problems, either fix them directly or add them as tasks to the Tasks section."

**Archive completed todos** ([grow.md](../grow.md))

> "Read docs/todo.md. Move all entries from the Resolved section to docs/todo_archive.md (create it if it does not exist). Keep the same format. Leave the Resolved section header in todo.md but empty."


## Stage 3: Enforce

**Create a test plan** ([enforce.md](../enforce.md))

> "Read my AGENTS.md and review the test coverage. Create a test plan: which domain logic needs unit tests? Which adapters need their own tests? Add basic security tests. Set up the test suite to run in CI."

**Set up import enforcement** ([enforce.md](../enforce.md))

> "Read my AGENTS.md and the architecture rules. Set up import enforcement for this project. The rule is: domain/ must never import from adapters/ or application/. adapters/ may import from domain/. Fail the build if violated."

**Set up pre-commit hooks** ([enforce.md](../enforce.md))

> "Set up pre-commit hooks for this project: linter, formatter, import checker, and secret scanner. Make sure they run automatically before every git commit."

**Add an application layer** ([enforce.md](../enforce.md))

> "Read my AGENTS.md. My use cases are getting complex and mix orchestration with business logic. Introduce an application/ layer: extract use case orchestration from domain/ into application/use_cases.*. Domain should only contain pure logic. Application coordinates the steps and calls through ports. Update the import rules accordingly."

**Migrate to formal ADRs** ([enforce.md](../enforce.md))

> "Migrate my docs/decisions.md to individual ADR files under docs/adr/. Create 0001-template.md as a reusable template. For each active decision, create a numbered ADR file with: Date, Status, Context, Decision, Consequences."

**Split AGENTS.md into path-specific rules** ([enforce.md](../enforce.md))

> "My AGENTS.md is over 80 lines. Split the architecture rules into .claude/rules/ files: one for domain/, one for adapters/, one for tests/. Each file should declare its path filter and contain only the rules relevant to that area. Keep AGENTS.md short."

**Set up branch protection** ([enforce.md](../enforce.md))

> "Set up branch protection for main: require pull requests, require at least one approval, require all CI checks to pass before merging. Create a CONTRIBUTING.md that explains the branching workflow."

**Set up CI/CD pipeline** ([enforce.md](../enforce.md))

> "Set up a CI pipeline (GitHub Actions / GitLab CI / your platform) that runs on every push: linter, formatter, import enforcement, secret scanner, and the full test suite. Block merges to main if any check fails."

**Create operations documentation** ([enforce.md](../enforce.md))

> "Read my AGENTS.md and understand how this project is deployed and run. Create docs/operations.md with the sections that apply. Skip sections that do not apply to this project type."

**Run the review checklist** ([enforce.md](../enforce.md))

> "Read my AGENTS.md and review the project against this checklist: (1) no secrets in code or git history, (2) input validation at all boundaries, (3) dependencies up to date, (4) no DB/API calls inside loops, (5) error states visible to the user, (6) all commits scoped to their task, (7) no architecture boundary violations. Report findings sorted by severity."


## Security

**Audit .gitignore and git history for secrets** ([security.md](security.md))

> "Review my .gitignore and make sure it excludes files that might contain credentials. Check for: .env, .env.*, *.key, *.pem, *.pfx, *.p12, *.jks, secrets/, config.local.*, *.sqlite, *.db, .npmrc, .pypirc, .docker/config.json, terraform.tfstate. Also check git history for accidentally committed secrets."

**Dependency audit** ([security.md](security.md))

> "Run a dependency audit. Check for known vulnerabilities in all dependencies. List any that are outdated or have known CVEs. Suggest updates, noting any breaking changes that I should review before applying."

**Check for prompt injection risks** ([security.md](security.md))

> "Review my code for prompt injection risks. Check every place where user input is combined with LLM prompts. Make sure user input is clearly separated from system instructions and cannot override them."

**Verify dependencies are real** ([security.md](security.md))

> "Review my requirements.txt / package.json. For each dependency, verify it exists on PyPI/npm, check when it was last updated, and flag any with fewer than 100 downloads or no maintainer activity in the past year."

**Review authorization** ([security.md](security.md))

> "Review my API endpoints. For each endpoint, check: is authentication required? Is authorization checked (does the user have permission to access *this specific resource*, not just *any resource*)? Flag any endpoint where a user could access another user's data by changing an ID in the URL."

**Quick security scan** ([security.md](security.md))

> "Review my project for the most critical security issues: secrets in code or git history, missing input validation, SQL injection risks, XSS vulnerabilities, and error messages that leak internal details. Report only critical findings. Do not fix anything, just report."

**Full security review** ([security.md](security.md))

> "Read my AGENTS.md and review the entire codebase for security issues. Check: no secrets in code or config files, all user input validated at the adapter boundary, output escaping in templates (no raw/unescaped user data in HTML), database queries use parameterized statements, password hashing uses bcrypt/argon2 (not MD5/SHA256), error messages do not leak internal details, logs do not contain passwords or tokens, dependencies are up to date, CSRF protection on state-changing endpoints, security headers set, authentication and authorization enforced on network-accessible endpoints, CORS configured restrictively. Create a report with findings sorted by severity. Do not fix automatically. Discuss fixes with me before applying."

**Pre-release security hardening** ([security.md](security.md))

> "This project is about to be released. Run a security hardening pass: check all OWASP Top 10 2021 categories against this codebase, verify that secrets management is correct, test input validation and output escaping at every boundary, check for missing rate limiting, verify HTTPS is enforced, review error handling for information leakage, check access control on every endpoint, verify password hashing. Create a detailed report with findings and recommended fixes."

**Set up automated security scanning** ([security.md](security.md))

> "Set up automated security scanning for this project: add a secret scanner to pre-commit hooks (detect-secrets, gitleaks, or trufflehog), enable security linting rules in the existing linter, and add dependency vulnerability scanning (pip-audit for Python, npm audit for Node.js). Make sure these checks run before every commit and in CI."


## Performance

**Find the bottleneck** ([performance.md](performance.md))

> "My project is slow but I do not know where the bottleneck is. Add timing measurements to the main operations: database queries, API calls, file operations, and data processing. Log each with its duration in seconds. Then tell me which operations take the longest."

**Review database queries** ([performance.md](performance.md))

> "Review all database queries in this project. For each query: does it have a LIMIT and ORDER BY? Would it benefit from an index? Is it called inside a loop (N+1 risk)? Does it fetch columns that are not used? Suggest specific indexes and query improvements."

**Check crash recovery** ([performance.md](performance.md))

> "Review my project for crash recovery issues. Check: what happens if the program crashes mid-operation? Are there half-written files, stale locks, or orphaned 'running' state? Are write operations atomic (temp file + rename)? Can the program restart safely without duplicating work?"

**Quick performance check** ([performance.md](performance.md))

> "Review my project for performance issues. Check: all database queries have LIMIT and ORDER BY, no expensive operations inside loops, all external calls have timeouts, large data uses streaming instead of loading into memory. Report findings. Do not fix automatically."

**Full performance review** ([performance.md](performance.md))

> "Read my AGENTS.md and review the codebase for performance issues. Check: database queries have appropriate indexes, no N+1 query patterns, all external calls have configurable timeouts, large data processed via streaming or pagination, resources cleaned up after use, retry logic uses exponential backoff with jitter, caching used where data is read often but changes rarely. Report findings sorted by impact."


## AI Workflow

**Start a session** ([ai-workflow.md](../ai-workflow.md))

> "Read AGENTS.md and docs/todo.md. What was I working on? What is the most important open item?"

**End a session** ([ai-workflow.md](../ai-workflow.md))

> "Update docs/todo.md with what we accomplished and what is still open. If we made any decisions, add them to docs/decisions.md. Summarize what the next session should start with."

**Capture learnings** ([ai-workflow.md](../ai-workflow.md))

> "What were the key learnings from this session? What surprised us? What would we do differently next time? Format as short bullet points I can add to my learning journal."

**Analyze a past project for patterns** ([ai-workflow.md](../ai-workflow.md))

> "Analyze the project at [path]. Look at git history, folder structure, AGENTS.md, and docs. What patterns were used? What worked well? What caused problems? What can we learn for our current project?"


## Architecture Alternatives

**Migrate one tangled file (Strangler Fig)** ([triggers.md](triggers.md))

> "Read my AGENTS.md and understand the project. I want to migrate to a domain/adapters structure using the Strangler Fig approach. Do not rewrite everything at once. Pick the one file where business logic and infrastructure are most tangled. Extract the business logic into domain/ and the infrastructure code into adapters/. Create the port interface in domain/. Wire them together in main. Fix imports. Run the tests. Then stop and let me review before moving to the next file."

**Reorganize into feature slices** ([architecture-patterns.md](architecture-patterns.md))

> "Read my AGENTS.md. My domain/ folder has grown too large with unrelated models. Reorganize the project into feature-sliced architecture: create a features/ folder with one subfolder per feature area. Each feature gets its own domain/, adapters/, and tests/. Move shared types to shared/. Update imports."

**Convert to modular monolith** ([architecture-patterns.md](architecture-patterns.md))

> "Read my AGENTS.md. I want to convert this project to a modular monolith. Create a modules/ folder. Each module gets its own api/ (public interface), application/, domain/, and adapters/. Modules may only communicate through each other's api/. No direct access to another module's domain or adapters. Update imports and add import rules."

**Reorganize into vertical slices** ([architecture-patterns.md](architecture-patterns.md))

> "Read my AGENTS.md. Reorganize this project into vertical slices: one folder per user-facing operation under features/. Each slice gets its own handler, validator (if needed), and test. Shared logic goes into shared/. No shared service layer."

**Which architecture fits my project?** ([architecture-patterns.md](architecture-patterns.md))

> "Read my AGENTS.md and analyze the project structure. Which files change together most often? Are there feature areas that could be isolated? Would the project benefit from feature-sliced, modular monolith, or vertical slice architecture? Explain why."
