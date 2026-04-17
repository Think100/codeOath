# TODO

## Tasks

- [x] `3-soon` ai-code-review.md "Your Review Workflow" section: release pipeline / commit workflow feels out of place in the guide. Find a better structure or move to its own section
- [ ] `3-soon` languages/rust.md: human review by Rust-experienced person (correctness of current best practices, new Testing and Common Pitfalls sections, tone consistency with python.md)
- [ ] `3-soon` resources/build-pipeline.md: human review by CI/CD practitioner (GitHub Actions example correctness, pre-commit config accuracy, CD/signing details, stage-based recommendations)
- [x] `4-later` languages/rust.md mapping table
- [ ] `4-later` languages/javascript.md and languages/typescript.md mapping tables
- [ ] `4-later` Enforcement examples (JS/TS only): eslint-plugin-boundaries config, when language guides exist
- [x] `4-later` Pre-commit hook examples for non-Python languages
- [ ] `3-soon` Frontend/UI guide: how React/Vue/Svelte components map to the domain/adapters model. Include: multilingual UI patterns (i18n, string externalization, language switching)
- [ ] `6-waiting` CONTRIBUTING.md: PR submissions currently not open, feedback via Issues only. When PRs open: add CC BY 4.0 contribution clause
- [ ] `3-soon` End-user documentation guide: separate guide for generating user-facing docs (README, user guide, feature descriptions, getting started for non-devs). Complement to auto-documentation.md which covers developer docs
- [ ] `5-routines` prompts.md: check if sorting still works when new prompts are added (currently clean)
- [ ] `5-routines` Root README reference length: watch for >20 guides, introduce sub-pages if needed
- [ ] `5-routines` FAQ length: watch (currently 6, threshold ~8, then move to docs/faq.md)
- [ ] `5-routines` Code quality heuristics: guide with simple metrics to detect drift (file size trends, import depth, decision frequency). No tools, just heuristics and questions
- [ ] `6-waiting` grow.md H2 "When Folders Are Not Enough": check if contrast to Concept 1-2 is strong enough (waiting for community/test user feedback)
- [ ] `3-soon` Guide für Multi-Sprachen-Projekte: wie strukturiert man Projekte mit mehreren Programmiersprachen (z.B. Python-Backend + TypeScript-Frontend)? Grenzen, Ordnerstruktur, wo liegen Adapter/Domain pro Sprache, wie hält man Konventionen konsistent
- [x] `3-soon` Guide zum sauberen Einführen von Lintern: wie führt man Linter (ruff, eslint, etc.) in bestehenden Projekten ein, ohne tagelang Warnungen abzuarbeiten. Schrittweises Onboarding, Baseline-Dateien, gezielte Regelaktivierung, Fokus auf neue Commits statt Big-Bang-Fix

## Open Questions

- [ ] `6-waiting` Text pipelines as a separate track?
      Context: Different project type with its own core questions (idempotency, resume, artifact management)
