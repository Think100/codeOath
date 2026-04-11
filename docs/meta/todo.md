# TODO

## Tasks

- [ ] `3-soon` ai-code-review.md "Your Review Workflow" Sektion: Release-Pipeline/Commit-Workflow fuehlt sich deplatziert im Guide. Bessere Struktur finden oder in eigenen Abschnitt auslagern
- [ ] `4-later` languages/rust.md mapping table
- [ ] `4-later` languages/javascript.md and languages/typescript.md mapping tables
- [ ] `3-soon` Enforcement examples: eslint-plugin-boundaries config (JavaScript/TypeScript, when language guides exist)
- [ ] `4-later` Pre-commit hook examples for non-Python languages
- [ ] `3-soon` Frontend/UI guide: how React/Vue/Svelte components map to the domain/adapters model. Include: multilingual UI patterns (i18n, string externalization, language switching)
- [ ] `6-waiting` CONTRIBUTING.md: PR submissions currently not open, feedback via Issues only. When PRs open: add CC BY 4.0 contribution clause
- [x] `1-now` Auto-documentation: prompt recipe or minimal script that generates full project documentation from codebase structure, docstrings, and README fragments
- [ ] `4-later` Git recovery patterns: branch-per-session, squash workflow, what to do when AI breaks the architecture. Low priority, review when opportunity arises
- [x] `1-later` Flow diagram generator: prompt recipe or minimal script that produces Mermaid flow diagrams (architecture, call flows, data flows) from project structure and code
- [ ] `3-soon` End-user documentation guide: separate guide for generating user-facing docs (README, user guide, feature descriptions, getting started for non-devs). Complement to auto-documentation.md which covers developer docs
- [ ] `5-routines` prompts.md: check if sorting still works when new prompts are added (currently clean)
- [ ] `5-routines` Root README reference length: watch for >20 guides, introduce sub-pages if needed
- [ ] `5-routines` FAQ length: watch (currently 6, threshold ~8, then move to docs/faq.md)
- [ ] `5-routines` Code quality heuristics: guide with simple metrics to detect drift (file size trends, import depth, decision frequency). No tools, just heuristics and questions
- [ ] `6-waiting` grow.md H2 "When Folders Are Not Enough": check if contrast to Concept 1-2 is strong enough (waiting for community/test user feedback)

## Open Questions

- [ ] `6-waiting` Text pipelines as a separate track?
      Context: Different project type with its own core questions (idempotency, resume, artifact management)

- [ ] `6-waiting` Context window management guide?
      Context: Currently relevant (2026): AGENTS.md line limits, path-specific rule loading, navigation hints, large-file offsets. Will become less important as context windows grow. Could be an AI-specific guide that ages out, or a section in enforce.md. Fits the "Maturity Dial" concept in philosophy.md.
