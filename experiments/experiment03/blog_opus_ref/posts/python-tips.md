---
title: Three Python Tips I Use Every Day
date: 2026-03-27
tags: python, programming
---

Here are three small Python patterns that I reach for constantly.

## 1. Dictionary unpacking for defaults

```python
defaults = {"timeout": 30, "retries": 3}
config = {**defaults, **user_config}
```

This merges two dictionaries, with `user_config` values taking priority.

## 2. The walrus operator

```python
if (n := len(items)) > 10:
    print(f"Too many items: {n}")
```

Assign and test in one expression. Available since Python 3.8.

## 3. pathlib over os.path

```python
from pathlib import Path

data = Path("data")
for csv in data.glob("*.csv"):
    print(csv.stem)
```

`pathlib` makes file operations more readable and less error-prone.
