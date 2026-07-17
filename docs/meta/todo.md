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
- [ ] `5-routines` Code quality heuristics: guide with simple metrics to detect drift (file size trends, import depth, decision frequency). No tools, just heuristics and questions
- [ ] `6-waiting` grow.md H2 "When Folders Are Not Enough": check if contrast to Concept 1-2 is strong enough (waiting for community/test user feedback)
- [ ] `3-soon` Multi-language project guide: how to structure projects with multiple programming languages (e.g. Python backend + TypeScript frontend). Boundaries, folder structure, where domain/adapters live per language, how to keep conventions consistent
- [x] `2-next` security.md relevance navigation: add a mini-nav after the TL;DR (Local tool / Web app / Multi-user / Cloud) and a "Only relevant if..." line at the start of each advanced section (Multi-Tenant, JWT/OAuth, Cloud Hardening), so Stage 1 readers do not drown in enterprise content (done 2026-07-17, commit ae8c705)
- [ ] `4-later` Payment guide: accepting payments in vibe-coded apps. Never handle card data yourself (PCI scope), use a hosted checkout (Stripe, Paddle, Lemon Squeezy), webhooks for payment status, test mode before going live
- [ ] `4-later` Logging strategy guide: log levels (DEBUG/INFO/WARN/ERROR), structured logs, correlation IDs, proactive info logging beyond errors. Stage 3+ topic; complements the existing "errors must be visible" rule
- [x] `3-soon` docs/meta/decisions.md: restore reverse-chronological order (2026-03-31 and 2026-03-29 entries sit below older ones at the end of the file) (done 2026-07-06, commit 550d19b)
- [x] `3-soon` docs/resources/triggers-draft.md: compare against triggers.md with fresh eyes (vibecoder-language rewrite, all triggers as observable symptoms instead of architecture diagnoses). Decide: replace triggers.md or discard the draft (done 2026-07-07, draft replaced triggers.md; diagnose prompt added to prompts.md)
- [ ] `4-later` templates/ folder with copy-paste starter files (AGENTS.md variants per project type, todo.md, decisions.md). Insight from repo comparison (ai-dev-tasks, awesome-cursorrules): successful repos deliver copy-paste artifacts, not reading material. Deliberately deferred: guides still change too often, templates would need constant syncing with them (decided 2026-07-06)
- [ ] `3-soon` README entry path: show the result before asking to read. Terminal cast or GIF of the Stage 1 setup at the top of the README, goal: a visitor understands the value in 5 minutes without reading a guide
- [x] `3-soon` (done 2026-07-06, new section "Keep Configuration in One Place") grow.md: configuration and secrets section is missing (config/ appears in the structure tree but is never explained; original text lost, see CHANGELOG 0.3.0). Cover: all settings in one place (config/), main reads config and passes values to domain (domain never reads env or files itself), validate at startup (fail fast). Secrets: never in checked-in files; .env + .gitignore + AI deny rule (.claude/settings.json) because .gitignore does not stop AI agents reading the file; .env.example pattern as documentation; password manager as source of truth. Keep proportional: no secret-manager CLI workflows, that is beyond the audience

## Open Questions

- [ ] `6-waiting` Text pipelines as a separate track?
      Context: Different project type with its own core questions (idempotency, resume, artifact management)
