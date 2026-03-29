# codeOath

Architecture governance guide for AI-assisted development.

## NOT

- Not a framework (no installable package, no runtime dependency)
- Not a linter (guides toward linters, does not replace them)
- Not for enterprise scale (solo to small team, up to ~20 modules)
- Not rigid about architecture (recommends patterns per stage, user adapts)

## Rules

- Core docs (docs/) are language-free. No Python, no language-specific syntax.
- Language-specific content lives exclusively in `docs/languages/`
- Language adaptation happens via `docs/languages/<lang>.md`
- Pseudocode in docs uses C-style syntax (broadly readable across communities)
- Every claim about enforcement must reference a concrete tool or example
- Do not add features, tracks, or languages without updating ROADMAP.md

## Language Conventions

This repo is open-source, so English everywhere except internal docs.

| Artifact                | Language          | Why                                    |
|-------------------------|-------------------|----------------------------------------|
| Code (vars, functions)  | English           | Universal, libraries expect it         |
| Code comments           | English           | Same language as the code              |
| Commit messages         | English           | Git history searchable and consistent  |
| Core docs (docs/)       | English           | Open-source audience                   |
| Internal docs (meta/)   | English           | Consistent with core docs              |
| AGENTS.md               | English           | Open-source repo                       |
| README.md               | English           | Open-source repo                       |
| Experiments             | English           | Generated code, English prompts        |

## Structure

- `docs/` -- Core guide documents (language-neutral)
- `docs/resources/` -- Security, performance, testing, architecture, philosophy, prompts
- `docs/languages/` -- One mapping file per supported language
- `docs/meta/` -- Internal project files (todo, decisions, style guide)
- `experiments/` -- AI-generated code comparing with/without codeOath

## Documentation

- Roadmap and planned features: `ROADMAP.md`
- Change history: `CHANGELOG.md`
- Open tasks and questions: `docs/meta/todo.md`
