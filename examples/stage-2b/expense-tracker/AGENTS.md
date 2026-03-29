# expense-tracker

CLI tool to log and summarize personal expenses from the terminal. Stores data locally as JSON.

## NOT
- Not a GUI or web app (terminal is enough for one user, no server complexity)
- Not multi-user (single local data file, no auth needed)
- Not a budgeting tool (no limits, forecasts, or alerts -- just log and view)
- Not synced to any cloud or bank (manual entry only, no integrations)

## Rules
- Python 3.14+
- Code and comments in English
- Data stored in a single JSON file (default: `~/.expense-tracker.json`)
- No secrets in code or version control
- New files: ask first (AI rule)
- New dependencies: ask first (AI rule)
- Commit after each completed task (AI rule)
- Prefix commits with tool name: [claude], [cursor], [codex] (AI rule)
- When uncertain: ask, don't guess (AI rule)

## Architecture
```
domain/    core logic, no external imports
adapters/  database, API, files, UI
main       connects domain and adapters
```

Rule: adapters may use domain. Domain must never use adapters.

- `domain/models.py`: Expense dataclass (frozen=True, slots=True)
- `domain/ports.py`: ExpenseRepository Protocol
- `domain/services.py`: pure functions (add_expense, summarize)
- `adapters/db.py`: JsonExpenseRepository -- implements the port
- `adapters/cli.py`: argparse CLI -- calls services, uses repo
- `main.py`: composition root -- wires repo + CLI

## Structure
- Source: expense_tracker/
- Tests: tests/ (test_domain.py for pure logic, test_adapters.py for file I/O)
- Docs: docs/
- Decisions: docs/decisions.md
- Tasks and open questions: docs/todo.md
