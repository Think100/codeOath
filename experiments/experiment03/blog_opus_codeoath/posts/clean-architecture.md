---
title: Why Clean Architecture Matters for Small Projects
date: 2025-03-10
tags: architecture, software-design
---

People often say clean architecture is overkill for small projects. I disagree, but with a caveat: **proportional architecture** matters more than any specific pattern.

## The Core Idea

Keep your domain logic (the "what") separate from your infrastructure (the "how"). Your business rules should not know whether data comes from a database, a file, or an API.

## Proportional Means Practical

For a small blog engine, you do not need:

- A full CQRS setup
- Event sourcing
- Microservices

What you *do* need:

- A clear boundary between "blog post logic" and "file reading"
- Contracts (interfaces/protocols) at the boundary
- Dependencies pointing inward (infrastructure depends on domain)

## The Payoff

Even in a 200-line project, this separation means:

- You can test domain logic without touching the filesystem
- Swapping Flask for another framework touches zero domain code
- New developers understand the codebase faster

It is not about the size of the project. It is about the clarity of thought.
