# TODO

## Tasks
- [x] Project structure and AGENTS.md
- [x] Expense model (add, list, summary)
- [x] JSON storage
- [x] CLI (add, list, summary commands)
- [x] Tests for core logic

## Open Questions
- [ ] Should `list` support filtering by month?
      Context: Currently shows all expenses. Might get noisy after months of use.
      Priority: nice to have, not blocking

## Resolved
- [x] SQLite or JSON for storage? -> JSON (no dependency, simple enough for one user)
- [x] Categories: fixed list or free text? -> Free text (simpler, no maintenance)
