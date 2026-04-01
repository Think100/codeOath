> [README](../../README.md) > [Docs](../) > **Architecture Patterns**

# Architecture Patterns

> **TL;DR (reference)** -- When domain/ grows too large or features keep colliding: feature-sliced (organize by feature area), modular monolith (hard module boundaries with public APIs), or vertical slices (one folder per user operation). All three work with codeOath's stages. Choose what fits, not what sounds impressive. You only need this when the default layered architecture no longer fits.

This is a reference, not a requirement. You only need this if the default layered architecture (domain/adapters) no longer fits your project. Most projects never get here.

If you are in Stage 1, skip this entirely. If you are in Stage 2 and things work fine, skip this too. Come back when the [triggers](triggers.md) tell you to.


## When the Default Is Not Enough

codeOath's default path is a layered architecture (Hexagonal Architecture, see [domain-and-adapters.md](domain-and-adapters.md)). It organizes code by technical role: logic vs. infrastructure. This works well when:

- The project has one clear domain area
- Changes tend to cut across layers (new feature = new domain model + new adapter)
- The team is small and everyone understands all parts

It starts to struggle when:

- Different features need different conventions
- Changes to one feature keep touching files in another
- The domain/ folder grows into a catch-all with dozens of unrelated models


## Feature-Sliced Architecture

Organize by feature instead of by technical layer. Each feature gets its own domain/, adapters/, and tests/.

```text
myproject/
├── features/
│   ├── orders/
│   │   ├── domain/
│   │   ├── adapters/
│   │   └── tests/
│   ├── billing/
│   │   ├── domain/
│   │   ├── adapters/
│   │   └── tests/
│   └── notifications/
│       ├── domain/
│       ├── adapters/
│       └── tests/
├── shared/
└── main
```

**When to use:** When work is organized by feature. When different features evolve independently. When AI should work within one feature without affecting others.

**Trade-off:** Stronger feature isolation, but shared concepts (user model used by orders and billing) need a `shared/` area that must be kept small.

> "Read my AGENTS.md. My domain/ folder has grown too large with unrelated models. Reorganize the project into feature-sliced architecture: create a features/ folder with one subfolder per feature area. Each feature gets its own domain/, adapters/, and tests/. Move shared types to shared/. Update imports."


## Modular Monolith

Like feature-sliced, but with harder boundaries between modules. Each module has its own public API (a defined interface that other modules use). No module may reach into another module's internals.

```text
myproject/
├── modules/
│   ├── orders/
│   │   ├── api/           <- public interface for other modules
│   │   ├── application/
│   │   ├── domain/
│   │   └── adapters/
│   ├── customers/
│   │   ├── api/
│   │   ├── application/
│   │   ├── domain/
│   │   └── adapters/
│   └── billing/
│       ├── api/
│       ├── application/
│       ├── domain/
│       └── adapters/
├── shared/
└── main
```

**When to use:** When modules must not reach into each other's internals. When the project might eventually split into separate services. When multiple people work on different modules simultaneously.

**Trade-off:** More structure, more discipline. Needs boundary enforcement (import linters, see [enforce.md](../enforce.md)) to be effective. Without automated checks, the boundaries will be violated.

> "Read my AGENTS.md. I want to convert this project to a modular monolith. Create a modules/ folder. Each module gets its own api/ (public interface), application/, domain/, and adapters/. Modules may only communicate through each other's api/. No direct access to another module's domain or adapters. Update imports and add import rules."


## Vertical Slices

Each user-facing operation is its own slice. Often command/query oriented (one file or folder per action the user can perform). No shared service layer.

```text
myproject/
├── features/
│   ├── create_order/
│   │   ├── handler
│   │   ├── validator
│   │   └── test
│   ├── get_order_details/
│   │   ├── handler
│   │   └── test
│   └── cancel_order/
│       ├── handler
│       ├── validator
│       └── test
└── shared/
```

**When to use:** UI-driven applications with clear user actions. When each operation is relatively independent. When you want changes to affect only one slice at a time.

**Trade-off:** Very local changes (one slice = one feature), but shared domain logic can lead to duplication or a growing `shared/` area.

> "Read my AGENTS.md. Reorganize this project into vertical slices: one folder per user-facing operation under features/. Each slice gets its own handler, validator (if needed), and test. Shared logic goes into shared/. No shared service layer."


## How to Choose

| Your situation | Consider |
|----------------|----------|
| Small project, one domain area | Layered (codeOath default) |
| Multiple independent feature areas | Feature-sliced |
| Features need hard boundaries and separate APIs | Modular monolith |
| UI-driven with clear user operations | Vertical slices |
| Project outgrowing 20+ modules | Split into separate projects |

These are not mutually exclusive. A layered project can adopt feature-slicing for one area. A modular monolith can use vertical slices within a module. Choose what fits, not what sounds impressive.

Not sure which fits? Ask your AI:

> "Read my AGENTS.md and analyze the project structure. Which files change together most often? Are there feature areas that could be isolated? Would the project benefit from feature-sliced, modular monolith, or vertical slice architecture? Explain why."


## Relationship to codeOath Stages

codeOath's three stages (Start, Grow, Enforce) work with any of these architectures. The stages describe how much governance you add, not which architecture you use.

- **Stage 1** works with any architecture (or none)
- **Stage 2** introduces the layered default, but you can use feature-sliced instead if it fits your project better
- **Stage 3** adds enforcement, which applies to any architecture that has boundaries to enforce

If you switch architectures, update your AGENTS.md to reflect the new structure. Your AI needs to know the rules.
