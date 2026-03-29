---
title: On Simplicity in Software
date: 2026-03-20
tags: [software, design, philosophy]
---

# On Simplicity in Software

The hardest thing in software is not solving a complex problem. It is keeping the solution simple.

## Complexity creeps in

Every added abstraction, every new dependency, every "just in case" branch adds weight. Over time, the system becomes hard to understand, hard to test, hard to change.

## Simple does not mean easy

A simple design requires more thought upfront. You have to understand the problem deeply before you can find the minimal solution. The shortcut is usually to add more code.

## A practical heuristic

Before adding something, ask: what breaks if I leave this out? If the answer is "nothing yet", leave it out. You can always add it when the need is concrete.

> Make things as simple as possible, but not simpler.
