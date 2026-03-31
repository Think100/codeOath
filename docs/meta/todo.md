# TODO

## Tasks

- [ ] CONTRIBUTING.md: PR submissions currently not open, feedback via Issues only. When PRs open: add CC BY 4.0 contribution clause
- [x] Examples: "How to run" instructions per stage — checked: AI-helps-you messaging is covered multiple times in start.md, grow.md, and README.md
- [x] Examples README: add model/date note ("These results reflect Claude Sonnet as of March 2026", Opus feedback)
- [ ] `6-waiting` grow.md H2 "When Folders Are Not Enough": pruefen ob Kontrast zu Concept 1-2 stark genug (waiting for community/test user feedback)
- [x] start.md Copilot/Cursor/Claude Code one-liner examples — re-checked: clear and concise as-is
- [ ] languages/rust.md mapping table
- [ ] languages/javascript.md and languages/typescript.md mapping tables
- [ ] Enforcement examples: eslint-plugin-boundaries config (JavaScript/TypeScript, when language guides exist)
- [ ] Pre-commit hook examples for non-Python languages
- [x] enforce.md: multi-language import enforcement with prompt recipe and script warning
- [x] Create release checklist (docs/resources/release-checklist.md): identity/legal, self-test, external test, code quality, security, performance, docs, repo hygiene, go/no-go. Human curated.
- [x] Review security.md checklist on correctness (human curated, verify after Python content move)
- [x] Review performance.md checklist on correctness (human curated, verify after Python content move)
- [ ] Frontend/UI guide: how React/Vue/Svelte components map to the domain/adapters model (next big feature)
- [x] Config management pattern: add "Configuration Pattern" section to docs/languages/python.md (config/.env + typed dataclass + startup validation + .gitignore)
- [ ] `4-later` Auto-documentation: prompt recipe or minimal script that generates a full project documentation from codebase structure, docstrings, and README fragments
- [ ] `4-later` Flow diagram generator: prompt recipe or minimal script that produces Mermaid flow diagrams (architecture, call flows, data flows) from project structure and code

## Open Questions

- [ ] Text pipelines as a separate track?
      Context: Different project type with its own core questions (idempotency, resume, artifact management)
      Priority: after Phase 2

- [ ] Context window management guide?
      Context: Currently relevant (2026): AGENTS.md line limits, path-specific rule loading, navigation hints, large-file offsets. Will become less important as context windows grow. Could be an AI-specific guide that ages out, or a section in enforce.md. Fits the "Maturity Dial" concept in philosophy.md.
      Priority: evaluate, may not be needed long-term
