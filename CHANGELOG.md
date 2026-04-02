# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.7.0] - 2026-04-02

### Added
- ai-code-review.md: error handling principles, five common AI code problems,
  review workflow with copy-paste prompts
- dependency-evaluation.md: when to add a library, three checks before install
  (real, maintained, license), when to remove

### Changed
- Experiments link in README "See It in Action" section
- codeOath version metadata to all experiment runs (Beta) and examples (0.1.0)
- experiments/README.md restructured: Results overview table and cross-run
  learnings before method and individual runs (results first, lab setup second)
- experiments/README.md: model names corrected to Sonnet 4.6 / Opus 4.6
- examples/README.md: model name corrected to Sonnet 4.6
- grow.md overhaul: Concept 1-4 texts simplified, testing intro rewritten,
  error/logging check prompt before separator, testing prompt focused on tests
  (static analysis removed)
- Multi-Agent Patterns added as section in ai-workflow.md
- Error handling guidance added to start.md (rule) and grow.md (Concept 1),
  linked to ai-code-review.md
- Dependency evaluation rule added to start.md, linked in grow.md routines table
- enforce.md: ai-code-review.md linked at audit agents
- grow.md: dependency-evaluation and ai-code-review linked in routines table
- README: references to ai-code-review.md and dependency-evaluation.md added
- README: broken anchor #already-have-a-project fixed
- README: footer cleaned up (removed redundant GitHub URL)

## [0.6.0] - 2026-04-02

### Added
- Refactor vs. Rewrite decision guide in triggers.md: "When Starting Fresh Makes
  More Sense" with 5 signals (language change, bridges more expensive than migration,
  fundamental security flaw, no tests/understanding, dead technology) and
  second-system effect warning
- Cross-link from triggers.md migration section to grow.md shim pattern
- "All Guides" compact link section in README (replaces two reference tables)

### Changed
- README completely rewritten: new opening that explains what codeOath is without
  jargon ("Define your project in plain text"), Get Started before code example,
  proven-practices framing, no-install messaging moved to opening
- Renamed ports-and-adapters.md to domain-and-adapters.md (clearer for beginners)
- Renamed alternatives.md to architecture-patterns.md (clearer scope)
- Updated all references to renamed files across 10 documents
- triggers.md: TL;DR rewritten in plain language, tables formatted consistently,
  "costs nothing" softened to "low effort", 80% threshold replaced with
  qualitative signal
- Stage table: "New project" changed to "Any project" (existing projects welcome)
- See It in Action table: simplified from 3 columns to 2

### Removed
- Rebuild vs. fix guide from roadmap (now covered by triggers.md rewrite section)
- docs/README.md content overlap (root README is now the only index)

## [0.5.0] - 2026-03-29

### Added
- Expense-tracker example project across all stages (Stage 1, 2a, 2b, 3)
  with comparison table, prompts used, and progressive complexity
- "See It in Action" section in README with example links
- GitHub social preview template (docs/meta/github_social-preview.html)
- examples/README.md with walkthrough and at-a-glance comparison

### Changed
- README updated with example project showcase
- ROADMAP synced: example project and import-linter config marked done

## [0.4.0] - 2026-03-28

### Added
- TL;DR blocks for all 9 docs over 100 lines, with type tags (deep dive,
  practical guide, reference)
- Language conventions guide expanded: why section, edge cases table,
  bilingual project example, AI tool findings (~27 to ~130 lines)
- Inline jargon explanations at first mention: Strangler Fig, pre-commit hooks,
  CI/CD, shim, semaphore, ADR
- Routine frequency table in grow.md (suggested defaults per routine type)
- "You can stop here" break in python.md after Stage 2
- Pace layers disclaimer in philosophy.md ("not the same as the three stages")
- "One document to start" in README, sets expectation before reading
- security.md expanded: Authentication Deep Dive (OAuth, JWT, session vs token),
  Multi-Tenant Isolation (row-level security, two-tenant testing),
  Cloud Deployment Hardening (env vars, network segmentation, containers,
  metadata endpoint). Checklists extended.
- performance.md expanded: Distributed Caching (cache-aside, stampede prevention),
  Database Query Planning (EXPLAIN, common problems),
  Profiling Complex Systems (flame graphs, distributed tracing, 80/20 rule)

### Changed
- AGENTS.md: "Not rigid about architecture" replaces incorrect
  "Not prescriptive about architecture"
- performance.md: all 10 Python code blocks replaced with language-neutral
  pseudocode (core docs are now fully language-free)
- README reference section split into Practical vs Background (prevents
  philosophy.md being mistaken for required reading)
- Style-guide updated: TL;DR comes before intro line, type tags replace
  separate intro blockquotes, single blockquote format
- Merged duplicate blockquotes (deep dive/practical guide + TL;DR) into
  single TL;DR with type tag across 4 docs
- ROADMAP synced with todo.md, CLI idea removed (prompt does the same job)

## [0.3.0] - 2026-03-27

### Added
- Beginner onboarding: "Your AI can teach you" hint in start.md for Git/tools
- Commit hygiene section in start.md (snapshot analogy, commit-per-task rule)
- AI rules in AGENTS.md template: "New dependencies: ask first",
  "Commit after each completed task"
- Logging guidance in grow.md (adapter concern, not domain)
- Configuration guidance in grow.md (one place, domain receives params)
- `config/` folder in Stage 2 project structure
- Dependency injection explained in ports-and-adapters.md (after Composition Root)
- Error handling across boundaries in ports-and-adapters.md (domain vs.
  infrastructure errors, adapter translates)
- Two new Common Mistakes: silent try/catch, infrastructure errors leaking
  into domain
- Routines concept in grow.md (recurring maintenance tasks with last-done dates)
- Todo archive pattern in grow.md (keep todo.md focused)
- Operations documentation as Stage 3 menu item 10 (startup, monitoring,
  backup, retention, troubleshooting)
- Migration guidance and strangler fig prompt in triggers.md
- Experiments folder with AI architecture comparison
- .gitignore (secrets-only baseline)

### Changed
- Stage 2 concepts reordered: decisions (#2) before ports (#3), with explicit
  "you can stop here" breakpoint between simple and advanced concepts
- Stage 2 knowledge boundary statement: "Concepts 3 and 4 introduce software
  architecture, normally taught in courses or on the job"
- Stage 3 menu reordered by progression: builds-on-Stage-2 first, then
  project-growth items, then team items
- CI/CD moved to "when others contribute" group (no value over pre-commit
  hooks for solo vibe coding)
- Testing strategy moved to Stage 3 #1 (direct Stage 2 continuation)
- ADR framed as natural evolution of decisions.md, not new concept
- Stage 2 folder structure: ports removed from diagram (introduced at concept 3)
- README rewritten for clarity and flow
- start.md and grow.md rewritten for beginner accessibility
- enforce.md renamed from harden.md, framed as menu not checklist
- philosophy.md restructured for clarity, added proportionality principle
- alternatives.md improved, philosophy.md anchor fixed
- decisions.md format aligned with grow.md template
- Branding normalized: codeoath to codeOath throughout
- Line endings normalized to LF

## [0.2.0] - 2026-03-26

### Added
- Three-stage model: start, grow, enforce (replaces monolithic docs)
- Trigger-based migration path (docs/triggers.md)
- Ports and Adapters explanation with pseudocode (docs/ports-and-adapters.md)
- Architecture alternatives reference (docs/alternatives.md)
- Language mapping file (docs/languages/python.md)
- Copyable templates for minimal and layered projects
- AGENTS.md in root (codeOath dogfoods itself)
- CHANGELOG.md and ROADMAP.md
- Example todo.md with review checklists
- "Coming back to a project" sections in start.md and grow.md
- docs/decisions.md for dogfooding decision records
- Error-handling and async patterns in language mapping tables
- "AI Rules and Engineering Rules" section in philosophy.md (separates
  engineering fundamentals from AI-specific workarounds)
- AI Maturity Dial concept: AI-specific rules have an expiry date, revisit as
  models improve
- AI Tool Compatibility note in philosophy.md (works with any tool, examples
  use Claude Code)
- Common Mistakes section in ports-and-adapters.md (6 beginner-friendly
  examples of what can go wrong)

### Changed
- Philosophy doc shortened and made language-neutral
- Contracts: now recommends code-based enforcement instead of docstring headers
- "Structure is governance" claim now honestly scoped to Stage 3 with tooling
- Renamed "Three-Layer Governance Model" to "Pace Layers" (credit Stewart Brand)
- Stage 3 framed as "menu, not checklist" (pick what solves your problem)
- OOP bias in ports-and-adapters.md acknowledged with disclaimer
- Removed redundant explanations across docs (cross-references instead of
  repetition, -46 lines in Block A alone)
- AGENTS.md line guidance: generalized to ~80 lines instead of separate 40/80
  thresholds per stage
- Context window optimization: now a principle ("keep the context focused")
  instead of hard numbers, with cross-references from start/grow/enforce to
  philosophy.md
- Multi-model review process: 2 rounds, 22 agents total, 24 findings fixed

### Removed
- Monolithic docs: SETUP.md, structure.md, conventions.md, workflow.md,
  security.md, performance.md, scaling.md, project-definition.md
- Python-specific examples and terminology in core docs
- Docstring-based module contracts as primary recommendation
- Empty placeholder directories (examples/python/.gitkeep, templates/.gitkeep)

## [0.1.0] - 2026-03-22

### Added
- Initial release
- Philosophy document with five principles
- Project definition guide with NOT field concept
- Folder structure recommendation (layered architecture)
- Module contracts (docstring-based)
- AI governance layer (CLAUDE.md, AGENTS.md, .claude/rules/)
- Security and performance principles
- Scaling guide
- Workflow guide (commits, sessions, ADRs)
