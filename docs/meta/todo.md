# TODO

## Tasks

- [ ] CONTRIBUTING.md: PR submissions currently not open, feedback via Issues only. When PRs open: add CC BY 4.0 contribution clause
- [ ] grow.md Ueberarbeitung (in progress): Concept 1-4 Texte vereinfacht, Concept 4 Testing-Intro noch nicht fertig. Uncommittete Aenderungen in grow.md. Naechster Schritt: Concept 4 Einleitungssatz fixen, dann gesamtes File reviewen und committen
- [ ] `6-waiting` grow.md H2 "When Folders Are Not Enough": check if contrast to Concept 1-2 is strong enough (waiting for community/test user feedback)
- [ ] languages/rust.md mapping table
- [ ] languages/javascript.md and languages/typescript.md mapping tables
- [ ] Enforcement examples: eslint-plugin-boundaries config (JavaScript/TypeScript, when language guides exist)
- [ ] Pre-commit hook examples for non-Python languages
- [x] Multi-Agent Patterns: added as section in ai-workflow.md (practical principles, no separate guide)
- [x] Error handling in start/grow: rule in start.md, paragraph in grow.md Concept 1, link to ai-code-review.md
- [x] Dependency evaluation in start/grow: rule in start.md ("ask first, explain why"), grow.md Routines-Tabelle verlinkt
- [ ] ai-code-review.md "Your Review Workflow" Sektion: Release-Pipeline/Commit-Workflow fuehlt sich deplatziert im Guide. Bessere Struktur finden oder in eigenen Abschnitt auslagern
- [x] README: Referenzen auf ai-code-review.md und dependency-evaluation.md ergaenzen
- [x] README: broken anchor #already-have-a-project gefixt
- [x] enforce.md: ai-code-review.md bei Audit-Agents verlinkt
- [x] grow.md: dependency-evaluation und ai-code-review in Routines-Tabelle verlinkt
- [ ] `3-monitor` prompts.md: check if sorting still works when new prompts are added (currently clean)
- [ ] `3-monitor` Root README reference length: watch for >20 guides, introduce sub-pages if needed
- [ ] `3-monitor` FAQ length: watch (currently 6, threshold ~8, then move to docs/faq.md)
- [ ] Frontend/UI guide: how React/Vue/Svelte components map to the domain/adapters model. Include: multilingual UI patterns (i18n, string externalization, language switching) (next big feature)
- [ ] `4-later` Auto-documentation: prompt recipe or minimal script that generates full project documentation from codebase structure, docstrings, and README fragments
- [ ] `3-monitor` Code quality heuristics: guide with simple metrics to detect drift (file size trends, import depth, decision frequency). No tools, just heuristics and questions
- [ ] `4-later` Git recovery patterns: branch-per-session, squash workflow, what to do when AI breaks the architecture. Low priority, review when opportunity arises
- [ ] `4-later` Flow diagram generator: prompt recipe or minimal script that produces Mermaid flow diagrams (architecture, call flows, data flows) from project structure and code

## Open Questions

- [ ] Text pipelines as a separate track?
      Context: Different project type with its own core questions (idempotency, resume, artifact management)
      Priority: after Phase 2

- [ ] Context window management guide?
      Context: Currently relevant (2026): AGENTS.md line limits, path-specific rule loading, navigation hints, large-file offsets. Will become less important as context windows grow. Could be an AI-specific guide that ages out, or a section in enforce.md. Fits the "Maturity Dial" concept in philosophy.md.
      Priority: evaluate, may not be needed long-term
