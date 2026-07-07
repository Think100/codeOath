---
title: Learning Flask
date: 2026-02-03
tags: python, flask, web
---

## Getting started with Flask

Flask is a lightweight web framework for Python. It's a great fit for small
projects like this blog.

- Minimal boilerplate
- Jinja2 templates built in
- Easy routing

Here's a minimal app:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world!"
```

That's really all it takes to get a page on the screen.
