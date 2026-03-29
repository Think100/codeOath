# expense-tracker

A minimal CLI tool to track personal expenses from the terminal. Built as a Stage 3 example
for the [codeOath](https://github.com/your-org/codeoath) methodology.

---

## Installation

```bash
pip install -e ".[dev]"
```

Requires Python 3.14+.

---

## Usage

### Add an expense

```bash
expense add 12.50 "Coffee"
expense add 45.00 "Train ticket" --category transport
expense add 8.90 "Lunch" --category food --date 2026-03-28
```

### List expenses

```bash
expense list
expense list --category food
expense list --month 2026-03
```

### Delete an expense

```bash
expense delete 3f2d1a0e-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Summary

```bash
expense summary
expense summary --month 2026-03
```

---

## Configuration

The database is stored at `~/.expense_tracker/expenses.db` by default.
Override with the `EXPENSE_DB` environment variable or the `--db` flag:

```bash
EXPENSE_DB=/tmp/test.db expense list
expense --db /tmp/test.db list
```

---

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks (runs ruff and import-linter on every commit)
pre-commit install

# Run tests
pytest

# Lint and format
ruff check src tests
ruff format src tests

# Check import boundaries
lint-imports
```

---

## Architecture

The project follows a three-layer hexagonal architecture:

```
domain/       Pure business logic. No external imports. Models and abstract ports.
application/  Use cases. Orchestrates domain objects. No framework dependencies.
adapters/     Inbound (CLI via Click) and outbound (SQLite via sqlite3).
```

Import direction is strictly enforced:

```
adapters -> application -> domain
                        ^
                        |
                   (no upward imports)
```

Enforcement: `import-linter` configured in `pyproject.toml`, checked in pre-commit and CI.

For architectural decisions, see `docs/adr/`.
