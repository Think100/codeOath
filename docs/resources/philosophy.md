> [README](../../README.md) > [Docs](../) > **Philosophy**

# Philosophy

> **TL;DR (deep dive)** -- Five principles: (1) define before you build, (2) structure is governance, (3) lower layers never violate upper layers, (4) maintenance must be cheap, (5) convention over configuration. Architecture constrains what the AI can do wrong. Some rules are permanent engineering; others are temporary AI guardrails. Remove the guardrails when they stop being needed. You do not need this to use codeOath. Start with [start.md](../start.md), come back here for the *why*.

The thinking behind codeOath: why the principles exist, how they connect, and which ones will age out as AI improves.


## The Problem

Software projects lose consistency over time. This is not a bug, it is gravity.

With AI-assisted development, this gets specific: AI agents do what you ask, but they do not know where the boundaries are. Without clear boundaries, they build too broadly, mix patterns, expand scope, and introduce inconsistencies. Not because they are bad at coding, but because they optimize for "solve the current task" rather than "keep the project coherent."

After a few weeks, you have working code that nobody fully understands. Put the project aside for three months and you are lost in your own codebase.

These problems will get smaller as AI models improve. But they will not disappear. Good structure helps regardless of how smart the AI is.


## Five Principles

These are the foundation. Every decision in codeOath traces back to one of these.

1. **Define before you build.** A project without a definition drifts. Write down what the project is, what it is not, and what success looks like. If the definition keeps changing, the scope was never clear.

2. **Structure is governance.** Folder structure determines what your AI agent can see, touch, and where things belong. A clear structure makes bad decisions harder. A messy structure makes good decisions harder to find.

3. **Lower layers must never violate upper layers.** A daily decision that contradicts the project definition is invalid. A convention that undermines a core principle is wrong. Simple, absolute, and the single most effective protection against scope creep.

4. **Maintenance must be cheap.** If it takes more than two minutes, it will not get done. Every document, every convention, every check must be low-effort to maintain. Complexity that nobody maintains is worse than no structure at all.

5. **Convention over configuration.** When in doubt, follow the convention. Use the AGENTS.md template from [start.md](../start.md) instead of inventing your own format. When the convention is wrong, change it deliberately and document why.


## Pace Layers

**Not the same as the three stages.** Stages (Start/Grow/Enforce) describe *when* you add structure. Pace layers describe *what kind* of decisions you are making at any moment. Both have three levels, but they answer different questions.

Every project has three governance layers. Each layer changes at a different speed. This idea is inspired by Stewart Brand's Pace Layering concept (*The Clock of the Long Now*, 1999): systems are healthiest when their layers move at their natural pace.

```text
+-------------------------------------+
|  1. PROJECT DEFINITION              |  What is the project?
|     (almost never changes)          |  What is it NOT?
|                                     |  What principles always apply?
+-------------------------------------+
|  2. CONVENTIONS                     |  Patterns, boundaries,
|     (rarely changes)                |  structure, naming rules
|                                     |
+-------------------------------------+
|  3. DAILY WORK                      |  Decisions, TODOs,
|     (changes constantly)            |  current state, open questions
|                                     |
+-------------------------------------+
```

**Layer 1: Project Definition** is the anchor. What the project is. What it is not. The MVP. Quality principles. Written once, almost never changed.

**Layer 2: Conventions** are the rules. Architecture, boundaries, naming, contracts. Change rarely, and when they do, the change is deliberate and documented.

**Layer 3: Daily Work** is everything during development. Tasks, decisions, open questions. Changes constantly, and that is fine, as long as it never violates the layers above it.

The core rule: **Lower layers must never violate upper layers.** But the relationship is not one-way: daily work is how you *discover* that a convention needs updating, or that the project definition is incomplete. The slow layers constrain the fast layers; the fast layers propose changes to the slow layers. The key is that changes to upper layers are deliberate, not accidental.


## Fail Fast

If something is wrong, you want to know immediately, not after three weeks of building on a broken foundation.

This applies at every level:

- **Project definition:** If the scope is unclear, the first task will feel wrong. That is the signal. Stop and fix the definition before writing more code.
- **Architecture:** If a module does not fit into the layer structure, that is not a "we will fix it later" problem. It means the structure needs a decision now.
- **AI interaction:** If an AI agent produces output that contradicts your conventions, do not patch the output. Fix the instruction that allowed it.

The principle: **surface problems at the earliest possible moment.** The cost of fixing something grows with every layer built on top of it. A wrong project definition discovered on day one costs five minutes. Discovered after three months, it costs a rewrite.

Fail fast is not about failing often. It is about making failure cheap by catching it early.


## Feedback Loops

Structure without feedback is wishful thinking. You need signals that tell you when something drifts.

### Built-in Signals

These exist naturally if you follow codeOath:

- A task that does not fit any existing module means the structure may need a new boundary, or the task is out of scope.
- A decision that contradicts an earlier decision means one of them is wrong. Check `decisions.md`.
- An AI agent that keeps ignoring a convention means the convention is not where the agent can see it, or it is too vague to follow.

### Deliberate Checkpoints

- When a stage transition feels right, review the [triggers](triggers.md) before acting.
- When a convention is violated more than twice, it is either wrong or not enforceable. Decide which.
- When you return to a project after a break, read the project definition first. If it surprises you, something drifted.

The principle: **if you cannot tell that something is broken, you cannot fix it.** Feedback loops make drift visible before it becomes a rewrite.


## Architecture as Constraint

Most approaches to AI-assisted development treat consistency as a memory problem. codeOath treats it as an architecture problem: **if the structure itself enforces the rules, certain classes of mistakes become structurally impossible.**

This idea comes from layered architecture (often called hexagonal or ports and adapters): code organized in concentric rings, dependencies always pointing inward.

```text
Outer ring:  ADAPTERS    (database, API, UI, file system)
Middle ring: APPLICATION (use cases, orchestration)
Inner ring:  DOMAIN      (business rules, pure logic, no dependencies)
```

The inner ring knows nothing about the outer rings. It does not know whether data comes from a database or a file. It only knows the rules.

When your folder structure mirrors this architecture, a linter can enforce the import direction. That is not an instruction that can be ignored. It is a wall. It does not catch every possible mistake (an AI can still create files in unexpected places or duplicate logic), but it catches the most common one: domain code importing infrastructure.

Important: This wall only exists when you add enforcement tooling (Stage 3). At Stage 1 and 2, the structure helps but does not prevent violations automatically. Be honest about this distinction.

For a detailed explanation, see [ports-and-adapters.md](ports-and-adapters.md).

Architecture must be proportional to the problem. A 400-line editor does not need four use case classes and three layers of protocols. A 4000-line application might. The same principles apply at every scale, but the mechanisms change. At Stage 1, a single file with clear functions is enough. At Stage 2, separate files per layer. At Stage 3, enforced boundaries with tooling. Applying Stage 3 mechanisms to a Stage 1 project creates complexity without benefit, and complexity that exceeds the problem is just as much a violation of "Maintenance must be cheap" as no structure at all.


## Contracts in Code, Not in Comments

A comment that describes what a function does will drift from reality the moment someone changes the code without updating the comment. In solo projects without code review, this happens constantly.

The alternative: let the code express what it needs. Instead of a comment saying "this function needs a database connection," write a function that takes a narrow interface as a parameter. If the function takes a `ReadInvoices` interface, it cannot delete invoices, send emails, or touch anything else. The type system enforces this, not discipline.

If your language has no type system (Lua, plain JavaScript), use convention plus tests to enforce boundaries. The principle is the same: make the contract visible in the code structure, not in prose that nobody updates.

A brief comment explaining *what* a file does is fine. But the boundary enforcement belongs in code, not in prose. For concrete syntax, see [languages/python.md](../languages/python.md).


## AI Rules and Engineering Rules

Not every rule in codeOath exists for the same reason. Some are good engineering regardless of who writes the code. Others exist because current AI models have specific limitations. Knowing the difference matters, because one category is permanent and the other has an expiry date.

### Engineering Fundamentals

These rules apply whether a human, an AI, or both write the code:

- Import direction: dependencies always point inward (adapters to domain, never reverse)
- Domain has no external dependencies
- Contracts expressed in the type system, not in comments
- Input validation at the boundary
- No secrets in code or version control
- Decisions documented with date and reason

These will not change. They are good software engineering.

### AI-Specific Rules

These rules exist because current AI models work better with explicit constraints. They follow one principle:

> **Keep the context focused.** Give the AI exactly the rules and scope it needs for the current task. Not more. This is the same principle as briefing a human developer: you hand them their assignment, not the entire project handbook.

In practice this means:

- Keep AGENTS.md concise (currently ~200 lines is a good target)
- Extract detailed rules into path-specific files when AGENTS.md grows too long
- Move the project definition to a separate file when it crowds out the rules
- Mark AI-generated commits so they are distinguishable in the git log
- Tell the AI to ask before creating new files or guessing at ambiguous requirements

The specific numbers will change as models improve. The principle will not: focused context produces better results than dumping everything into one prompt.

### The Maturity Dial

AI models get better. Context windows grow. Instruction-following improves. This means some rules that are necessary today will become unnecessary tomorrow.

Think of it as a dial, not a switch:

- **As of this writing:** Models benefit from short, structured instruction files, explicit "do not" rules, and path-scoped rule loading to save context.
- **Near future:** Larger effective context and better instruction-following will make strict line limits less important. The principle "keep it focused" still applies, but the threshold moves.
- **Eventually:** Models that reliably follow project-level conventions from a single document will make most AI-specific rules redundant. The engineering fundamentals remain.

When you revisit your codeOath setup, ask: **"Is this rule here because it is good engineering, or because the AI needs the guardrail?"** If the AI no longer needs it, remove it. Do not accumulate rules out of habit.

### Hybrid Rules

Some rules are good engineering that become *more important* with AI:

- Writing a project definition (useful for any developer, essential for AI scope control)
- Folder structure as governance (good organization generally, but AI "sees" boundaries through folders)
- Tracking tasks and decisions in files (standard practice, but AI uses the same files for onboarding)

These will stay even when AI-specific rules fade. They just might need less emphasis.


## What codeOath Does Not Solve

**Team coordination.** Multiple people need processes, reviews, and communication tools beyond documentation.

**External dependencies.** APIs change. Libraries break. No internal governance protects against the outside world.

**Motivation.** No system helps when you do not want to work on the project anymore.

**Scaling beyond its limits.** codeOath works for solo plus AI, up to about 20 modules, on projects that run for weeks to months. Beyond that, split the project. That is not failure, it is evolution.


## Further Reading

The ideas in this document build on established work. These recommendations are curated for relevance to AI-assisted solo development, not as an exhaustive reading list.

**Note:** This list was compiled with AI assistance and has not been independently verified by a human reviewer. Titles, years, and descriptions may contain errors. Verify before citing in academic or professional contexts.

**Architecture and design:**

- Stewart Brand, *How Buildings Learn* (1994) and *The Clock of the Long Now* (1999) -- pace layers as a model for systems that change at different speeds (the concept originates in *How Buildings Learn*, drawing on Frank Duffy's "shearing layers")
- Alistair Cockburn, "Hexagonal Architecture" (2005, web article at alistair.cockburn.us) -- the ports and adapters pattern that codeOath builds on
- Eric Evans, *Domain-Driven Design* (2003) -- bounded contexts, domain purity, the vocabulary behind domain/adapter separation
- Robert C. Martin, *Clean Architecture* (2017) -- the Dependency Rule, concentric-ring architecture, layered dependency direction
- John Ousterhout, *A Philosophy of Software Design* (2nd ed., 2021) -- complexity reduction, deep modules, information hiding, simplicity as a design goal
- Jim Shore, "Fail Fast" (IEEE Software, 2004) -- the principle of surfacing problems at the earliest possible moment

**Practice and AI:**

- Tom Taulli, *AI-Assisted Programming* (O'Reilly, 2024) -- systematic approach to working with AI coding tools

---

This document described the thinking. The rest describes the doing: [start.md](../start.md), [grow.md](../grow.md), [enforce.md](../enforce.md), and everything in [resources/](.).
