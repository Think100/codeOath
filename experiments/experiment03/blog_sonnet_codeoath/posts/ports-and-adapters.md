---
title: Ports and Adapters at the Right Scale
date: 2026-03-25
tags: [architecture, python]
---

The ports-and-adapters pattern (also called hexagonal architecture) has a reputation for being over-engineered. That reputation is earned -- when people apply it to a 200-line script, it is.

But when applied proportionally, it solves a real problem: **your domain logic should not know where data comes from.**

## The pattern in one sentence

Define what you need as a Protocol (the port). Let infrastructure implement it (the adapter). Domain code only talks to the port.

## A minimal example

```python
# domain/ports.py -- the contract
from typing import Protocol
from .model import Post

class PostRepository(Protocol):
    def get_all(self) -> list[Post]: ...
    def get_by_slug(self, slug: str) -> Post | None: ...
```

```python
# infrastructure/file_repository.py -- the adapter
class FilePostRepository:
    def get_all(self) -> list[Post]:
        # reads from disk
        ...
```

The domain never imports `FilePostRepository`. Infrastructure imports from domain. Not the other way around.

## When does this pay off?

- When you want to test domain logic without touching the filesystem
- When you might swap the storage layer later
- When the codebase grows past one file

For a 50-line script: skip it. For a project with routes, templates, and persistence: worth it.
