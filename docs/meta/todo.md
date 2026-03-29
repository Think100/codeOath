# TODO

## Tasks

- [ ] CONTRIBUTING.md: PR submissions currently not open, feedback via Issues only. When PRs open: add CC BY 4.0 contribution clause
- [ ] Examples: "How to run" instructions per stage (pip install -e . or python -m, Sonnet review feedback)
- [ ] Examples README: add model/date note ("These results reflect Claude Sonnet as of March 2026", Opus feedback)
- [ ] grow.md H2 "When Folders Are Not Enough": eingefuegt, pruefen ob Kontrast zu Concept 1-2 stark genug
- [ ] start.md Copilot/Cursor/Claude Code one-liner examples: eingefuegt, pruefen ob klar genug
- [ ] languages/rust.md mapping table
- [ ] languages/javascript.md and languages/typescript.md mapping tables
- [ ] Enforcement examples: eslint-plugin-boundaries config (JavaScript/TypeScript, when language guides exist)
- [ ] Pre-commit hook examples for non-Python languages
- [ ] Create release checklist (docs/release-checklist.md): extract MVP hardening from enforce.md, cross-cutting checks (security, performance, docs completeness, architecture check) as a copyable checklist for projects that will be published
- [ ] Review security.md checklist on correctness (human curated, verify after Python content move)
- [ ] Review performance.md checklist on correctness (human curated, verify after Python content move)
- [ ] Frontend/UI guide: how React/Vue/Svelte components map to the domain/adapters model (next big feature)
- [ ] Config management pattern: add "Configuration Pattern" section to docs/languages/python.md (YAML + ENV override + typed dataclass + startup validation)

## Open Questions

- [ ] Text pipelines as a separate track?
      Context: Different project type with its own core questions (idempotency, resume, artifact management)
      Priority: after Phase 2

- [ ] Context window management guide?
      Context: Currently relevant (2026): AGENTS.md line limits, path-specific rule loading, navigation hints, large-file offsets. Will become less important as context windows grow. Could be an AI-specific guide that ages out, or a section in enforce.md. Fits the "Maturity Dial" concept in philosophy.md.
      Priority: evaluate, may not be needed long-term
