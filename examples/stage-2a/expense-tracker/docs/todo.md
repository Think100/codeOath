# Todo

## Open

- [ ] Add expense editing (update amount or description)
- [ ] Export to CSV
- [ ] Filter list by date range

## Routines

- [ ] Check docs match current code (last: 2026-03-29, every: 2 weeks)
- [ ] Update dependencies, check for known vulnerabilities (last: 2026-03-29, every: month)
- [ ] Security scan: no secrets in code, input validation at boundaries (last: 2026-03-29, every: month)

## Resolved

- [x] Domain/adapters split following Stage 2 structure
- [x] SQLite storage with Decimal-safe TEXT column
- [x] CLI: add, list, list --category, summary, delete
- [x] Short ID prefix matching for delete command
- [x] Domain tests (models, validation, summarize)
- [x] Adapter tests (save, list, find, delete, precision)
- [x] decisions.md with rationale for key choices
