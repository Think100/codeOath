# TODO

## Tasks
- [x] Project structure and AGENTS.md
- [x] Domain model (Expense, frozen dataclass)
- [x] Port (ExpenseRepository protocol)
- [x] Domain services (add_expense, summarize)
- [x] JSON adapter (JsonExpenseRepository)
- [x] CLI adapter (add, list, summary commands)
- [x] Composition root (main.py)
- [x] Tests: domain (pure logic) and adapters (file I/O)
- [x] docs/decisions.md

## Open Questions
- [ ] Should `list` support filtering by month or category?
      Context: Currently shows all expenses. Might get noisy over time.
      Priority: nice to have, not blocking

## Routines

- [ ] Check docs match current code (last: 2026-03-29, every: 2 weeks)
- [ ] Update dependencies, check for known vulnerabilities (last: 2026-03-29, every: month)
- [ ] Security scan: no secrets in code, input validation at boundaries (last: 2026-03-29, every: month)

## Resolved
- [x] SQLite or JSON for storage? -> JSON (no dependency, simple enough for one user)
- [x] Categories: fixed list or free text? -> Free text (simpler, no maintenance)
- [x] Architecture: flat or domain/adapters split? -> domain/adapters (Stage 2, see decisions.md)
