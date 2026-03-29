# Decisions

## 2026-03-28: Architecture must be proportional to the problem
**Status:** active
Experiment finding: Opus with codeOath built 10 files with full ports-and-adapters for a 400-line text editor but forgot basic features. Sonnet with 4 files scored higher. Over-engineering is as much a violation of "Maintenance must be cheap" as no structure at all. Added proportionality paragraph to philosophy.md.

## 2026-03-28: Security and Performance as standalone cross-cutting guides
**Status:** active
Extracted security and performance from enforce.md into docs/resources/. They apply from Stage 1, not just Stage 3. Keeps enforce.md focused on enforcement tooling. Both guides written with "why" explanations for vibe coders.

## 2026-03-28: Philosophy.md marked as deep dive, not required reading
**Status:** active
Vibe coder review found that philosophy.md in the main navigation path scared beginners away. Marked as optional with "start with start.md, come back here when you want to understand why."

## 2026-03-28: Experiments folder for reproducible AI architecture comparisons
**Status:** active
Standardized experiment format: identical prompt, one variable (with/without codeOath), scoring rubric (0-12). Two runs completed. Findings fed back into docs (proportionality, fail fast, error handling).

## 2026-03-28: Todo/Roadmap/Changelog separation
**Status:** active
Clear ownership: todo.md = internal working tasks, ROADMAP.md = public planned features only, CHANGELOG.md = release history. No duplication. Done items from todo go to CHANGELOG at release time, then get deleted from todo.

## 2026-03-27: Rename "Three-Layer Model" to "Pace Layers"
**Status:** active
The governance model (Project Definition / Conventions / Daily Work) and the
migration model (Start / Grow / Enforce) both used "three" and "layer/stage"
in their names. Renamed the governance model to "Pace Layers", inspired by
Stewart Brand's Pace Layering concept (*The Clock of the Long Now*, 1999).
The term describes layers that change at different speeds, which maps directly
to Definition (slow), Conventions (medium), and Daily Work (fast).

## 2026-03-26: Three stages with trigger-based migration
**Status:** active
Structure codeOath as three stages (Start/Grow/Enforce) where each stage adds
structure only when real symptoms appear. No file-count thresholds. The user
moves to a higher stage when they feel the pain, not because a document says so.

## 2026-03-26: Language-neutral core with language mapping files
**Status:** active
Core docs use pseudocode, no Python or TypeScript syntax. Language-specific
details (folder structure, port syntax, tooling) live in separate mapping
files under `languages/`. This avoids the credibility problem of claiming
"language-neutral" while showing only Python examples.

## 2026-03-25: CC BY-NC-SA 4.0 license
**Status:** replaced by 2026-03-29 decision

## 2026-03-29: CC BY 4.0 license (replaces NC-SA)
**Status:** active
NonCommercial was blocking adoption without providing real protection (ideas
are not copyrightable regardless of license). ShareAlike discouraged companies
from adapting the framework internally. CC BY 4.0 keeps attribution (the only
thing that matters for a methodology) and removes all other restrictions.
