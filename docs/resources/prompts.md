> [README](../../README.md) > [Docs](../) > **Prompt Cheatsheet**

# Prompt Cheatsheet

> **TL;DR** -- Copy-paste prompts for every stage: Stage 1 (project setup), Stage 2 (migration, testing, maintenance), Stage 3 (enforcement, CI/CD). Plus AI code review, dependency evaluation, security, performance, workflow, and architecture alternatives. No explanations here, see linked source docs for context.

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

> "Read my AGENTS.md. My use cases mix orchestration with business logic. Introduce an application/ layer: extract use case orchestration from domain/ into application/use_cases.*. Domain should only contain pure logic. Update the import rules accordingly."

**Migrate to formal ADRs** ([enforce.md](../enforce.md))

> "Migrate my docs/decisions.md to individual ADR files under docs/adr/. Create 0001-template.md as a reusable template."

**Split AGENTS.md into path-specific rules** ([enforce.md](../enforce.md))

> "My AGENTS.md is over 80 lines. Split the architecture rules into .claude/rules/ files: one for domain/, one for adapters/, one for tests/. Each file should declare its path filter and contain only the rules relevant to that area. Keep AGENTS.md short."

**Set up branch protection** ([enforce.md](../enforce.md))

> "Set up branch protection for main: require pull requests, require at least one approval, require all CI checks to pass before merging."

**Set up CI/CD pipeline** ([enforce.md](../enforce.md))

> "Set up a CI pipeline that runs on every push: linter, formatter, import enforcement, secret scanner, and the full test suite. Block merges to main if any check fails."

**Create operations documentation** ([enforce.md](../enforce.md))

> "Read my AGENTS.md. Create docs/operations.md with the sections that apply to this project. Skip sections that do not apply."

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

> "What were the key learnings from this session? What surprised us? What would we do differently next time? What worked well that we should keep doing? Were there any aha moments where something suddenly made sense?"

**Something is broken** ([ai-workflow.md](../ai-workflow.md))

> "[paste the full error message here]. What does this mean and how do I fix it?"

If more context is needed:

> "I was trying to [what you did]. I expected [what should happen]. Instead, [what actually happened]. Here is the error: [paste error]. What is wrong?"

**Multi-perspective review roles** ([ai-workflow.md](../ai-workflow.md))

> "You are a user who just installed this for the first time. Try to follow the README and use the main features. Where do you get stuck? What is confusing? What error messages are unhelpful?"

> "You are a senior fullstack developer with 20 years of experience. Review this for correctness, completeness, and dangerous simplifications. Cite line numbers."

> "You are a red team security auditor. Find vulnerabilities. Sort by severity (Critical, High, Medium, Low)."

> "You are a computer science professor. Check if the concepts are explained correctly. Suggest analogies that make complex ideas accessible."

> "You are a vibe coder with 2 months of experience. Read this guide. Where do you get lost? Where would you stop reading?"

**Multiple agents: check for file conflicts** ([ai-workflow.md](../ai-workflow.md))

> "I want to run a review while you keep working. Which files are you currently changing? I will make sure the review agent does not touch those."

**Analyze a past project for patterns** ([ai-workflow.md](../ai-workflow.md))

> "Analyze the project at [path]. Look at git history, folder structure, AGENTS.md, and docs. What patterns were used? What worked well? What caused problems? What can we learn for our current project?"


## AI Code Review

**Check for hidden errors** ([ai-code-review.md](ai-code-review.md))

> "Review the code you just wrote. Is there any place where an error is caught and ignored? Any place where the code continues as if nothing happened after something went wrong? I want errors to be visible, not hidden. Show me every place where a problem could happen silently."

**After every AI response that writes code** ([ai-code-review.md](ai-code-review.md))

> "Before we continue: check what you just wrote. Are there hidden errors (failures that I would not notice)? Unnecessary checks (for things that cannot happen)? Fallback values that could give me wrong results? Be honest, not defensive."

**Check for fake safety** ([ai-code-review.md](ai-code-review.md))

> "Look at the code you just wrote. Are there checks for impossible situations? For example: checking if a value is missing when you just created it one line above, or checking the type of something that already has a fixed type. Remove the checks that can never trigger. Explain which ones you removed and why they were unnecessary."

**Check for wrong fallbacks** ([ai-code-review.md](ai-code-review.md))

> "Check the code for fallback values. Are there places where the code returns a default (like an empty list, zero, or a blank value) when the real data is not available? For each case, tell me: is the fallback actually safe, or could it cause wrong results? If missing data means something is broken, the code should stop, not guess."

**Check for retry without limits** ([ai-code-review.md](ai-code-review.md))

> "Does the code retry anything (network calls, database connections, sending emails)? If yes: is there a maximum number of attempts? What happens after the maximum is reached? If there is no limit, add one. Three retries is a good default. After that, stop and report the error."

**Check for functions that do too much** ([ai-code-review.md](ai-code-review.md))

> "Look at the code you just wrote. Is there any function or block that does more than one job? For example: a function that validates input AND saves to the database AND sends an email. Split these into separate pieces. Each piece should do one thing. If one piece fails (email sending), the other pieces (saving the order) should not be affected."

**Check if AI built what you asked for** ([ai-code-review.md](ai-code-review.md))

> "Compare what you just built against what I asked for. List every requirement I gave you, and for each one, tell me: is it fully implemented, partially implemented, or missing? Then list everything you added that I did not ask for. I want an honest comparison, not a summary of what you built."

**Full AI code review before release** ([ai-code-review.md](ai-code-review.md))

> "Read AGENTS.md. Then review the entire codebase in six passes and report findings for each: 1. Hidden errors: where can something fail without me knowing? 2. Fake safety: where are there checks for impossible situations? 3. Wrong assumptions: where does the code guess instead of fail? 4. Scope: is everything I asked for implemented? Is there anything I did not ask for? 5. Secrets: any credentials in the code? 6. Structure: does the code follow the architecture rules in AGENTS.md? Do not fix anything. Report only. I will decide what to fix."


## Dependency Evaluation

**Should I use a library?** ([dependency-evaluation.md](dependency-evaluation.md))

> "I need to [describe the problem]. Should I use a library for this, or can you write a small solution directly? If a library, which one and why? How many dependencies does it bring with it? If not, write the solution and explain it."

**Verify a package is real** ([dependency-evaluation.md](dependency-evaluation.md))

> "Before installing [package name]: verify that this package actually exists on the official package registry for my language. Show me the official page, the number of downloads, and when it was last published. If you are not 100% certain it exists, say so."

**Check if a library is maintained** ([dependency-evaluation.md](dependency-evaluation.md))

> "Check the health of [package name]. When was the last release? When was the last commit? How many open issues are there, and are maintainers responding? How many maintainers are there? Would you call this actively maintained?"

**Check license compatibility** ([dependency-evaluation.md](dependency-evaluation.md))

> "What license does [package name] use? Is it compatible with [your project's license, e.g., MIT, CC BY 4.0]? Are there any restrictions I need to know about? If the license is GPL or AGPL, explain what that means for my project."

**Review all dependencies** ([dependency-evaluation.md](dependency-evaluation.md))

> "Review my dependency list. For each library, tell me: what do we actually use from it? Could we replace it with a small amount of custom code? Are any libraries unused or barely used? Which ones would you recommend removing, and why?"

**Check version pinning** ([dependency-evaluation.md](dependency-evaluation.md))

> "Show me all dependencies in this project with their exact versions. Are any unpinned or using version ranges? If so, pin them."


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
