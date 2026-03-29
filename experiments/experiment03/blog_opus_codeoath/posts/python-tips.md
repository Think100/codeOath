---
title: Three Python Tips I Use Every Day
date: 2025-02-14
tags: python, tips
---

Here are three small Python patterns that I reach for constantly.

## 1. Unpacking with `*`

```python
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]
```

## 2. Dictionary merge with `|`

Since Python 3.9 you can merge dicts with the pipe operator:

```python
defaults = {"color": "blue", "size": 10}
overrides = {"size": 20}
config = defaults | overrides
# {"color": "blue", "size": 20}
```

## 3. `pathlib` over `os.path`

`pathlib.Path` reads much more naturally:

```python
from pathlib import Path

config = Path("~/.config/myapp/settings.json").expanduser()
if config.exists():
    data = config.read_text()
```

Small things, big difference in readability.
