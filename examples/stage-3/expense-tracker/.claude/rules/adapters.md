# Rules: adapters/

## Inbound (adapters/inbound/)
- Handles user-facing input: CLI arguments, HTTP requests, etc.
- Validate and convert raw input to domain types before calling use cases.
- Call `application/use_cases.py` -- never call domain directly for orchestration.
- Raise framework-specific errors (e.g., `click.ClickException`) here, not in domain.

## Outbound (adapters/outbound/)
- Implements the abstract ports defined in `domain/ports.py`.
- No business logic here -- only persistence mechanics (SQL, file I/O, HTTP calls).
- Use transactions where appropriate and handle rollback on failure.

## Import direction
- Adapters may import from `domain/` and `application/`.
- `domain/` and `application/` must never import from `adapters/`.
- This is enforced by import-linter (pyproject.toml) and pre-commit.

## Error handling
- Log or surface errors at this layer, not in domain or application.
- Convert domain `ValueError` to user-friendly messages.
