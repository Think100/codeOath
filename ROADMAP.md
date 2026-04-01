# Roadmap

What is planned, what comes next, and what might happen eventually. For what already shipped, see [CHANGELOG.md](CHANGELOG.md).


## Now

What is done or actively being worked on for the next release.

- Multi-Agent Patterns: coordinating multiple AI agents (write permissions, conflict avoidance, orchestrator patterns)
- Debugging with AI: how to describe bugs, read stacktraces, and steer the AI toward a fix
- Dependency evaluation: when to add a library, how to check if a package is trustworthy
- Code review of AI output: what to check when reviewing AI-generated code as a non-programmer


## Next

Planned, but not started yet.

- Language mapping tables (JavaScript, TypeScript, Rust)
- eslint-plugin-boundaries config (JavaScript/TypeScript)
- Pre-commit hook examples for non-Python languages
- Frontend/UI guide: how React/Vue/Svelte components map to the domain/adapters model
- CONTRIBUTING.md: contribution workflow when PRs open
- Auto-documentation: prompt recipe that generates project documentation from codebase structure, docstrings, and README fragments
- Flow diagram generator: prompt recipe that produces Mermaid flow diagrams from project structure and code


## Later

Ideas we want to explore. No timeline, no commitment.

- Text pipelines as a dedicated project type / track
- Community-contributed language packs
- Video walkthrough of the three stages
- API design guide: how to structure endpoints following the domain/adapters model
- Code quality heuristics: simple metrics to detect project drift over time
- More languages based on demand (C++, Go, Lua)
- Project templates (cookiecutter/copier per language/stage), likely unnecessary as AI scaffolding improves
