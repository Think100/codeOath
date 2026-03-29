# Decisions

## 2026-03-29: Hexagonal architecture (domain/adapters/main)
**Status:** active
Domain logic in `domain/`, storage and CLI in `adapters/`, `main.py` wires them together.
Keeps AI-generated code in the right place: domain has no external imports. Adapter can be swapped (e.g. SQLite) without touching logic.

## 2026-03-29: typing.Protocol for ExpenseRepository port
**Status:** active
Python structural typing -- the adapter does not need to inherit from the port. Checked by mypy.
Simpler than ABC inheritance, idiomatic for Stage 2 Python projects.

## 2026-03-29: frozen=True for Expense model
**Status:** active
Expense is an immutable value object. No mutation after creation prevents subtle bugs.
Aligns with Stage 2 Python convention (`@dataclass(frozen=True, slots=True)`).

## 2026-03-29: JSON for storage
**Status:** active
Single-user, local data, no server needed. No dependency, human-readable file.
Revisit if concurrent access or large data sets become a requirement.

## 2026-03-29: Free text categories
**Status:** active
Simpler than a fixed list: no maintenance, user defines their own categories.
Downside: typos create duplicate categories. Acceptable for single-user use.

## Known Risks

| Risk | Mitigation |
|---|---|
| JSON does not handle concurrent writes safely | Single user, no concurrent access expected |
| Category typos create duplicate entries | Acceptable for personal use; add normalization if it becomes a problem |
| No input validation for amount (negative values accepted) | Add validation in services.py if needed |
