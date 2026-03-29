# expense-tracker

CLI tool to track personal expenses from the terminal.

## NOT
- Not a GUI (CLI is enough for one user)
- Not a web service (local only, no server complexity)
- Not a multi-user system (single-user SQLite, no auth needed)
- Not a budgeting system (tracking only, no limits or alerts)

## Rules
- Python 3.14+
- Code and comments in English
- No secrets in code or version control
- New files: ask first (AI rule)
- Prefix commits with your tool name: [claude], [cursor], [codex] (AI rule)
- When uncertain: ask, don't guess (AI rule)

## Architecture
```
domain/    core logic, no external imports
adapters/  database (SQLite), CLI (argparse)
main       connects domain and adapters
```

Rule: adapters may use domain. Domain must never use adapters.

## Structure
- Source: `expense_tracker/` (domain/, adapters/, main.py)
- Tests: `tests/`
- Docs: `docs/`
- Decisions: `docs/decisions.md`
- DB: `expenses.db` by default; override with `EXPENSE_DB` env var
