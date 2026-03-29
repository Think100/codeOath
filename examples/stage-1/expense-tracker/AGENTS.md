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

## Structure
- Source: expense_tracker/
- Tests: tests/
- Docs: docs/
- Tasks and open questions: docs/todo.md
