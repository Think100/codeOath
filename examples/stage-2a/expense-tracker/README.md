# expense-tracker

Track your expenses from the terminal.

## Setup

```bash
uv sync
```

## Usage

```bash
uv run expense-tracker add --amount 12.50 --category food --description "lunch"
uv run expense-tracker add --amount 2.80 --category transport --description "bus" --date 2026-03-28
uv run expense-tracker list
uv run expense-tracker list --category food
uv run expense-tracker summary
uv run expense-tracker delete <id>
```

The database is stored as `expenses.db` in the current directory. Override with the `EXPENSE_DB` environment variable.

## Tests

```bash
uv run pytest
```

## Stage

Built following [codeOath](../../..) Stage 2 (`grow.md`): domain/adapters split, decisions documented.
