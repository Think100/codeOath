# Roadmap

What is planned, what comes next, and what might happen eventually. For what already shipped, see [CHANGELOG.md](CHANGELOG.md).


## Now

What is done or actively being worked on for the next release.

- [ ] Text pipelines as a dedicated project type / track
- [ ] Build pipeline guide: CI/CD basics, when to automate, what a minimal pipeline looks like for AI-assisted projects

## Next

Planned, but not started yet.

- Frontend/UI guide: how React/Vue/Svelte components map to the domain/adapters model
- Building AI into your app: how to integrate LLMs (Claude, OpenAI, local models) into the software you are building - API basics, prompt patterns for in-app use, cost and safety
- Language mapping tables (JavaScript, TypeScript, Rust)
- Code quality heuristics: simple metrics to detect project drift over time
- eslint-plugin-boundaries config (JavaScript/TypeScript)
- Pre-commit hook examples for non-Python languages
- CONTRIBUTING.md: contribution workflow when PRs open


## Later

Ideas we want to explore. No timeline, no commitment.

- Community-contributed language packs
- Video walkthrough of the three stages
- API design guide: how to structure endpoints following the domain/adapters model
- Information flow guide: how data moves through a program (inputs, state, events, outputs), information architecture for AI-assisted projects
- More languages based on demand (C++, Go, Lua)
- Project templates (cookiecutter/copier per language/stage), likely unnecessary as AI scaffolding improves
- End-user documentation guide: user guides, feature descriptions, getting-started pages, and in-app help (tooltips, contextual help, onboarding flows). Explicitly out of scope in auto-documentation.md, needs its own guide with different failure modes.
- Language selection guide for vibecoders: which programming language fits which kind of project (web app, script, data tool, mobile, game). Focused on vibecoding trade-offs: AI support quality per language, ecosystem maturity, deployment simplicity, not on benchmarks or theory.
