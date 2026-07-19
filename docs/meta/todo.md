# TODO

## Tasks

- [ ] `3-soon` resources/build-pipeline.md: human review by CI/CD practitioner (GitHub Actions example correctness, pre-commit config accuracy, CD/signing details, stage-based recommendations)
- [ ] `4-later` languages/javascript.md and languages/typescript.md mapping tables
- [ ] `4-later` Enforcement examples (JS/TS only): eslint-plugin-boundaries config, when language guides exist
- [ ] `3-soon` Frontend/UI guide: how React/Vue/Svelte components map to the domain/adapters model. Include: multilingual UI patterns (i18n, string externalization, language switching)
- [ ] `6-waiting` CONTRIBUTING.md: PR submissions currently not open, feedback via Issues only. When PRs open: add CC BY 4.0 contribution clause
- [ ] `3-soon` End-user documentation guide: separate guide for generating user-facing docs (README, user guide, feature descriptions, getting started for non-devs). Complement to auto-documentation.md which covers developer docs
- [ ] `5-routines` prompts.md: check if sorting still works when new prompts are added (currently clean)
- [ ] `5-routines` Root README reference length: watch for >20 guides, introduce sub-pages if needed
- [ ] `5-routines` FAQ length: watch (currently 6, threshold ~8, then move to docs/faq.md)
- [ ] `6-waiting` grow.md H2 "When Folders Are Not Enough": check if contrast to Concept 1-2 is strong enough (waiting for community/test user feedback)
- [ ] `3-soon` Multi-language project guide: how to structure projects with multiple programming languages (e.g. Python backend + TypeScript frontend). Boundaries, folder structure, where domain/adapters live per language, how to keep conventions consistent
- [ ] `4-later` Payment guide: accepting payments in vibe-coded apps. Never handle card data yourself (PCI scope), use a hosted checkout (Stripe, Paddle, Lemon Squeezy), webhooks for payment status, test mode before going live
- [ ] `4-later` Logging strategy guide: log levels (DEBUG/INFO/WARN/ERROR), structured logs, correlation IDs, proactive info logging beyond errors. Stage 3+ topic; complements the existing "errors must be visible" rule
- [ ] `4-later` templates/ folder with copy-paste starter files (AGENTS.md variants per project type, todo.md, decisions.md). Insight from repo comparison (ai-dev-tasks, awesome-cursorrules): successful repos deliver copy-paste artifacts, not reading material. Deliberately deferred: guides still change too often, templates would need constant syncing with them (decided 2026-07-06)
- [ ] `3-soon` README entry path: show the result before asking to read. Terminal cast or GIF of the Stage 1 setup at the top of the README, goal: a visitor understands the value in 5 minutes without reading a guide

## Open Questions

- [ ] `6-waiting` Text pipelines as a separate track?
      Context: Different project type with its own core questions (idempotency, resume, artifact management)
