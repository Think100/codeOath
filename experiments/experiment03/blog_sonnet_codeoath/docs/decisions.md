# Architecture Decisions

## ADR-001: File-based post storage

**Status:** Accepted

**Context:** Posts need to be stored somewhere. Options: database, files.

**Decision:** Store posts as Markdown files in posts/. Filename encodes the slug. Front matter (YAML) holds metadata (title, date, tags).

**Reason:** Simple, no dependencies, human-readable, fits problem size.

---

## ADR-002: Flask as web framework

**Status:** Accepted

**Context:** Need an HTTP server to serve HTML pages locally.

**Decision:** Use Flask. It is the smallest reasonable web framework for Python that does not require configuration.

**Reason:** Standard library HTTP server has no templating. Flask is widely available, minimal, and well-known.

---

## ADR-003: Ports and adapters, proportional to size

**Status:** Accepted

**Context:** README.md requires clean separation: domain vs. infrastructure.

**Decision:** PostRepository is a Protocol (port). FilePostRepository is the adapter. Domain has no imports from infrastructure.

**Reason:** Keeps the domain testable without a filesystem. Does not over-engineer -- no DI container needed at this scale.
