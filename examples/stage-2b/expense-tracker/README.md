# expense-tracker

Track personal expenses from the terminal.

## Setup

```bash
uv sync
```

## Usage

```bash
# Add an expense
uv run expense-tracker add 12.50 food "lunch at the office"

# List all expenses
uv run expense-tracker list

# Show totals per category
uv run expense-tracker summary
```

Data is saved to `~/.expense-tracker.json` by default. Use `--file PATH` to change it.

## Run tests

```bash
uv run pytest
```
