# Decisions

## 2026-03-29: SQLite instead of JSON or CSV
**Status:** active
SQLite. Single-user, local, no server required. Decimal amounts stored as TEXT to avoid floating-point precision loss.

## 2026-03-29: argparse instead of Click
**Status:** active
argparse. Standard library only, no extra dependency. Four commands is simple enough for stdlib.

## 2026-03-29: typing.Protocol for the repository port
**Status:** active
Protocol (structural typing) instead of ABC. Adapters satisfy the contract by shape, not by inheritance. Consistent with the python.md recommendation.

## 2026-03-29: Decimal for amounts
**Status:** active
Decimal instead of float. Float arithmetic is imprecise for money (0.1 + 0.2 != 0.3). Stored as TEXT in SQLite to preserve exact string representation.

## Known Risks

| Risk | Mitigation |
|---|---|
| SQLite does not handle concurrent writes | Single-user only, not a concern |
| No input length limits on description/category | Acceptable for personal use; add if needed |
| DB path from env var is not validated | Trust the user; validate if this becomes a shared tool |
