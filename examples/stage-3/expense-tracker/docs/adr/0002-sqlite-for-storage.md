# ADR 0002: SQLite for Storage

## Date
2026-03-29

## Status
active

## Context
The expense tracker needs persistent local storage. Three options were considered:

- **Flat file (JSON/CSV):** Simple to implement, human-readable, no dependencies.
  Downside: no query support, fragile under concurrent writes, manual serialization.
- **SQLite:** Relational, single file, zero server, included in Python stdlib (`sqlite3`).
  Supports SQL queries, transactions, and foreign keys.
- **PostgreSQL:** Full relational database with concurrent access and network support.
  Overkill for a single-user CLI tool; requires a running server.

## Decision
Use SQLite via the Python stdlib `sqlite3` module.

No ORM. Raw SQL keeps the adapter thin and the dependency list short.
The repository pattern (`ExpenseRepository` port) isolates SQLite from the rest of the codebase,
so switching storage is possible without touching domain or application code.

## Consequences
- No server to install or manage.
- Single `.db` file, easy to back up or move.
- No concurrent write access (single-user tool, this is acceptable).
- No external dependencies for storage.
- If concurrent access is ever needed, revisit and consider replacing the adapter with PostgreSQL
  or a lightweight server-based solution -- the port abstraction makes this straightforward.
