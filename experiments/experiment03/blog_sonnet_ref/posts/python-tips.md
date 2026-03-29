---
title: Three Python Tips I Use Every Day
date: 2026-03-10
tags: [python, tips, programming]
---

# Three Python Tips I Use Every Day

Here are three small Python patterns that make daily coding cleaner.

## 1. Use `enumerate` instead of range+index

```python
# Instead of this:
for i in range(len(items)):
    print(i, items[i])

# Do this:
for i, item in enumerate(items):
    print(i, item)
```

## 2. Use `get` with a default on dicts

```python
config = {"host": "localhost"}
port = config.get("port", 8080)  # returns 8080 if key missing
```

## 3. Pathlib over string concatenation

```python
from pathlib import Path

base = Path("data")
file = base / "posts" / "hello.md"  # works on all platforms
```

These are small things, but they add up over a full workday.
