# ADR 0003: Click for CLI

## Date
2026-03-29

## Status
active

## Context
The expense tracker needs CLI argument parsing. Three options were considered:

- **argparse (stdlib):** No external dependency. Verbose to write, less ergonomic UX,
  no auto-generated help grouping.
- **Click:** Decorator-based, well-established, excellent UX defaults (auto help, error messages,
  context passing). One external dependency.
- **Typer:** Built on Click, adds type-annotation-driven CLI generation.
  More magic, heavier dependency, less transparent for a small project.

## Decision
Use Click (>=8.1).

The decorator-based approach fits the project's size well. Click is widely used, well-documented,
and stable. The `@click.pass_context` pattern maps cleanly to passing the repository through the
command group without globals.

## Consequences
- One external runtime dependency (`click`).
- Good built-in help text generation and error handling.
- Typer would add stricter type safety on CLI inputs, but also more abstraction and complexity.
  Can be reconsidered if the CLI grows significantly.
- If Click is ever removed, only `adapters/inbound/cli.py` needs to change -- domain and
  application are unaffected.
