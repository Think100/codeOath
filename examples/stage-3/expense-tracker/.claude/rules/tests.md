# Rules: tests/

## File responsibilities
- `test_domain.py`: Pure unit tests. No I/O, no fixtures with real databases, no mocks of stdlib.
- `test_application.py`: Use `InMemoryRepo` (defined in the test file itself). No real database.
- `test_adapters.py`: Use `tempfile.TemporaryDirectory` for real SQLite. Clean up after each test.

## General rules
- Never share mutable state between tests (no module-level stores, no class-level fixtures that mutate).
- Each test is independent and can run in any order.
- Use `pytest.fixture` with function scope (default) unless there is a strong reason for a wider scope.

## Naming
- Preferred: `test_<what>_<condition>` (e.g., `test_delete_nonexistent`)
- Also fine: `test_<what>` when the condition is the happy path (e.g., `test_add_expense`)

## What NOT to do
- Do not import real adapters in `test_domain.py` or `test_application.py`.
- Do not write to the real filesystem or home directory in any test.
- Do not use `unittest.mock` unless there is no cleaner alternative.
