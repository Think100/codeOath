---
title: On Simplicity in Software
date: 2026-03-28
tags: architecture, opinion
---

> Simplicity is the ultimate sophistication. -- Leonardo da Vinci

Every project I have worked on that grew out of control had one thing in common: complexity was added before it was needed.

## YAGNI is underrated

"You Aren't Gonna Need It" is not about being lazy. It is about discipline. Writing only the code that solves today's problem forces you to understand that problem deeply.

## The cost of abstraction

Every abstraction has a cost: indirection, cognitive load, and maintenance. A good abstraction pays for itself many times over. A premature one just makes the codebase harder to navigate.

## What I try to do

- Start with the simplest thing that could work
- Refactor when a real pattern emerges, not a hypothetical one
- Delete code aggressively
- Measure before optimizing

Software that is easy to understand is software that is easy to change. And that matters more than almost anything else.
