# Rules: domain/

## Imports
- No imports from `adapters/`, `application/`, or any external library.
- Only Python stdlib is allowed (dataclasses, datetime, decimal, uuid, abc, etc.).

## Structure
- Business models go in `models.py`.
- Abstract interfaces (ports) go in `ports.py`.
- Do not add subpackages without discussion.

## Behavior
- Raise `ValueError` for invalid input (wrong amount, empty strings, etc.).
- Never log, never print, never write to disk.
- No side effects of any kind.

## Why
The domain layer is the core of the application. It must be testable in complete isolation,
without a database, without a CLI, without any framework. Keeping it dependency-free
guarantees this.
