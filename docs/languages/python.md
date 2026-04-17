> [README](../../README.md) > [Docs](../) > **Python Language Mapping**

# Python Language Mapping

> **TL;DR** -- Stage 1: `pyproject.toml` + `ruff` + `pytest`. Stage 2: `domain/` with `typing.Protocol` ports, `adapters/` with implementations, `@dataclass(frozen=True)` for models, `main.py` wires them. Stage 3: `import-linter` enforces boundaries. Security: `yaml.safe_load`, never `pickle` or `eval` on untrusted input, Bandit rules via ruff.

This file translates codeOath concepts into Python. If you read [start.md](../start.md) or [grow.md](../grow.md) and wondered "what does that look like in Python?", this is the answer.

You do not need to read this file front to back. Jump to the stage you are in.


## Concept Mapping

codeOath uses generic terms. Here is what they mean in Python:

| codeOath Concept       | Python Implementation                                  | When |
|------------------------|--------------------------------------------------------|------|
| Source folder           | `<projectname>/` with `__init__.py`                   | Stage 1+ |
| Build config            | `pyproject.toml`                                      | Stage 1+ |
| Tests                   | `pytest`, files: `tests/test_<module>.py`             | Stage 1+ |
| Linter + Formatter      | `ruff` (linting) and `ruff format` (formatting)       | Stage 1+ |
| Dependency management   | `uv` (recommended) or `pip` with pinned versions      | Stage 1+ |
| Type checker            | `mypy --strict` or `pyright`                          | Stage 2+ |
| Port / Interface        | `typing.Protocol` in `domain/ports.py`                | Stage 2+ |
| Immutable domain object | `@dataclass(frozen=True, slots=True)`                 | Stage 2+ |
| Boundary validation     | `pydantic.BaseModel` in adapter layer (never in domain) | Stage 2+ |
| Composition root        | `main.py`, manual wiring (no DI framework needed)     | Stage 2+ |
| Import enforcement      | `import-linter` (CI check)                            | Stage 3 |
| Dependency vulnerability | `pip audit`                                           | Stage 3 |
| Secret scanner          | `detect-secrets` or `gitleaks` (pre-commit hook)      | Stage 3 |
| Error handling          | Exceptions (standard Python approach)                 | All |
| Async pattern           | `asyncio`, `async`/`await`                            | When needed |

You do not need everything from this table on day one. Start with Stage 1 tools, add the rest when you move to Stage 2 or 3.


## Folder Structure by Stage

### Stage 1: One package, flat

Everything in one package. No layers, no separation. Good enough for small projects.

```text
myproject/
├── docs/
│   └── todo.md
├── myproject/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── .gitignore
├── pyproject.toml
├── AGENTS.md
└── README.md
```

Minimal `.gitignore` for Python projects:

```text
# secrets
config/.env

# bytecode
__pycache__/
*.pyc

# virtual environment
.venv/

# build artifacts
dist/
build/
*.egg-info/

# tool caches
.mypy_cache/
.pytest_cache/
.ruff_cache/
```

Minimal `pyproject.toml`:

```toml
[project]
name = "myproject"
version = "0.1.0"
requires-python = ">=3.14"

[tool.ruff]
line-length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]

[dependency-groups]
dev = ["pytest", "ruff"]
```

To run your project and tests:

```bash
uv sync                     # install dependencies
uv run python -m myproject  # run the project
uv run pytest               # run tests
```

### Configuration

Keep all settings in one place. Do not scatter `os.getenv()` calls across your code. In [grow.md](../grow.md), `config/` is where settings live. In Python, a typed dataclass works well for this.

Define your settings in `config/.env` (never committed to git):

```bash
# config/.env
DB_PATH=/data/app.sqlite
API_URL=https://api.example.com
MAX_RETRIES=3
DEBUG=false
```

Load them into a typed dataclass:

```python
# config/settings.py
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class AppConfig:
    db_path: Path                # where the database file lives on disk
    api_url: str                 # URL to an external service
    max_retries: int
    debug: bool

def load_config() -> AppConfig:
    """Load paths, URLs, and settings from environment variables.
    Fails fast on startup if required values are missing."""
    return AppConfig(
        db_path=Path(os.environ["DB_PATH"]),
        api_url=os.environ["API_URL"],
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        debug=os.getenv("DEBUG", "false").lower() == "true",
    )
```

Call `load_config()` once in `main.py` and pass the result to whatever needs it. Domain code never imports `config/` or reads environment variables directly; it receives values as parameters.

### Stage 2: Domain and adapters separated

Your core logic (`domain/`) is now separate from everything that talks to the outside world (`adapters/`). Why? Because your AI sees clear boundaries: in `domain/`, no database imports allowed. You can test your logic without a real database. You can swap SQLite for PostgreSQL without touching your logic. See [domain-and-adapters.md](../resources/domain-and-adapters.md) for the full explanation.

```text
myproject/
├── docs/
│   ├── todo.md
│   └── decisions.md
├── myproject/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── ports.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   └── cli.py
│   └── main.py
├── tests/
│   ├── test_domain.py
│   └── test_adapters.py
├── .gitignore
├── pyproject.toml
├── AGENTS.md
└── README.md
```

`__init__.py` files should be empty. Use explicit imports (`from myproject.domain.models import Order`) instead of re-exporting from `__init__.py`.

---

**You can stop here.** Stage 1 and 2 folder structures cover most Python projects. Everything below (ports, import enforcement, security and performance patterns) is reference material for when you need it.

---

### Stage 3: Enforced boundaries

Same structure as Stage 2, but with automated checks that prevent violations. Import rules are enforced by tooling, not by discipline.

```text
myproject/
├── docs/
│   ├── todo.md
│   ├── decisions.md
│   └── definition.md
├── myproject/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── ports.py
│   │   └── services.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── http.py
│   │   ├── db.py
│   │   └── email.py
│   └── main.py
├── tests/
│   ├── test_domain.py
│   └── test_adapters.py
├── .pre-commit-config.yaml
├── .gitignore
├── pyproject.toml
├── AGENTS.md
└── README.md
```


## Port Example

Ports are how your domain says "I need something from the outside world" without knowing who provides it. In Python, you define them as `typing.Protocol` classes.

The domain defines the contract:

```python
# domain/ports.py
from __future__ import annotations
from typing import Protocol
from myproject.domain.models import Order

class OrderRepository(Protocol):
    def find_by_id(self, order_id: str) -> Order | None: ...
    def save(self, order: Order) -> None: ...
```

An adapter implements the contract. It does not need to inherit from the Protocol. Python checks the method signatures automatically (structural typing):

```python
# adapters/db.py
from myproject.domain.models import Order

class SqlOrderRepository:
    """Implements OrderRepository with SQLite."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def find_by_id(self, order_id: str) -> Order | None:
        # SELECT FROM orders WHERE id = ?
        ...

    def save(self, order: Order) -> None:
        # INSERT INTO orders ...
        ...
```

The composition root (`main.py`) wires them together. This is the only place that knows about both domain and adapters:

```python
# main.py
from myproject.adapters.db import SqlOrderRepository
from myproject.domain.services import OrderService

repo = SqlOrderRepository("orders.db")
service = OrderService(repo)
```


## Import Enforcement (Stage 3)

Once your project grows, you want to make sure nobody accidentally imports from `adapters` inside `domain`. `import-linter` checks this automatically.

Add this to your `pyproject.toml`:

```toml
[tool.importlinter]
root_packages = ["myproject"]

[[tool.importlinter.contracts]]
name = "Layered architecture"
type = "layers"
layers = [
    "myproject.adapters",
    "myproject.application",
    "myproject.domain",
]
```

Note: in the `layers` contract, earlier entries may import from later entries, but not the other way around. So `adapters` can import from `domain`, but `domain` cannot import from `adapters`.

Run `lint-imports` in CI or as a pre-commit hook. If someone adds a wrong import, the build fails.


## Pre-Commit Hooks

Automated checks that run before each `git commit`. If a check fails, the commit is blocked. Install once (`pip install pre-commit && pre-commit install`), then every commit is checked automatically.

Minimal `.pre-commit-config.yaml` for a Python project:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

What each hook does:

- **ruff**: finds common mistakes in your code and auto-fixes many of them
- **ruff-format**: makes your code look consistent (indentation, spacing, quote style)
- **mypy**: checks that types match, for example that you don't pass a string where a number is expected (alternative: pyright, but requires a Node runtime)
- **gitleaks**: catches passwords or API keys accidentally written into the code before they enter Git

For general CI/CD context and the relationship between pre-commit and GitHub Actions, see [build-pipeline.md](../resources/build-pipeline.md).


## Security Patterns

These patterns address Python-specific security concerns. For general security principles (input validation, authentication, OWASP): [security.md](../resources/security.md).

### YAML Deserialization

Always use `yaml.safe_load()`, never `yaml.load()`. Why? The unsafe version can execute arbitrary Python code embedded in a YAML file. An attacker who controls a YAML file (config upload, API input) can run any code on your server.

### Pickle Deserialization

Never `pickle.load()` data from untrusted sources. Why? Like unsafe YAML, pickle can execute arbitrary code during deserialization. This is especially relevant in ML/AI projects where models are distributed as `.pkl` files. If you load a model from an unknown source, it can compromise your system.

Use `safetensors`, `torch.load(..., weights_only=True)`, or verified checksums from trusted sources instead.

### eval() and exec()

Never use `eval()`, `exec()`, or `compile()` with user input. Why? These execute arbitrary Python code. Even seemingly harmless input can import modules and run system commands.

```python
# An attacker submits this as "math expression":
eval("__import__('os').system('rm -rf /')")
```

### Subprocess Handling

When calling external commands, always use list arguments, never shell strings:

```python
# Bad: shell injection risk. user_filename could contain "; rm -rf /"
subprocess.run(f"convert {user_filename}", shell=True)

# Good: no shell, no injection
subprocess.run(["convert", user_filename])
```

### Temporary Files

Use `tempfile.mkstemp()` or `tempfile.NamedTemporaryFile()` for temporary files. Why? Manually creating files in `/tmp` with predictable names allows symlink attacks: an attacker creates a symlink at the expected path pointing to a sensitive file, and your program overwrites it.

### Constant-Time Comparisons

When comparing secrets (tokens, API keys), use `hmac.compare_digest()` instead of `==`. Why? Regular string comparison returns `False` as soon as it finds a mismatched character, which takes slightly different amounts of time depending on how many characters match. An attacker can exploit this to guess the secret one character at a time.

Note: this applies to token comparison only. For passwords, use bcrypt/argon2 (they handle constant-time comparison internally).

### Cryptographic Tokens

Use `secrets.token_hex(32)` or `secrets.token_urlsafe(32)` for generating tokens, session IDs, and CSRF tokens. Never use `random` (predictable, not cryptographically secure). Prefer `secrets` over `uuid4` for security-critical tokens (`uuid4` has less entropy: 122 bits vs. 256 bits).

### Security Linting

Enable Bandit rules in your linter. For ruff, add `"S"` to the selected rules in `pyproject.toml`:

```toml
[tool.ruff.lint]
select = ["E", "F", "B", "S", "UP"]
```

This catches hardcoded passwords, unsafe `subprocess` calls, missing `safe_load`, `eval()` usage, weak hash functions, and more.

### Dependency Auditing

```bash
pip install pip-audit
pip-audit
```

This checks all installed packages against known vulnerability databases. Add it to your CI pipeline.


## Performance Patterns

These patterns address Python-specific performance concerns. For general performance principles (caching strategy, database optimization, crash recovery): [performance.md](../resources/performance.md).

### functools.lru_cache

The simplest way to cache function results in Python. If a function is called multiple times with the same arguments, the result is returned from cache instead of recomputed.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_user_profile(user_id: int) -> dict:
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
```

The first call with `user_id=42` hits the database. Every subsequent call with `user_id=42` returns the cached result instantly. `maxsize` limits how many results are kept (oldest are evicted).

**Watch out:** cached results are never updated. If the user profile changes, the cache still returns the old version. Use `get_user_profile.cache_clear()` when data changes, or use a TTL-based approach for time-sensitive data.

### String Concatenation in Loops

Building a string with `+=` in a loop is O(n^2) in Python because each `+=` creates a new string and copies everything. With large strings or many iterations, this becomes very slow.

```python
# Bad: O(n^2), each += copies the entire string
result = ""
for line in lines:
    result += line + "\n"

# Good: O(n), builds once at the end
result = "\n".join(lines)
```

### Lazy Imports

Heavy libraries (numpy, torch, yt_dlp) can take significant time to import (hundreds of milliseconds to seconds). If your program does not always need them, import inside the function that uses them:

```python
def transcribe(audio_path):
    from faster_whisper import WhisperModel  # only imported when needed
    model = WhisperModel("base")
    return model.transcribe(audio_path)
```

Note: this goes against the Python convention of imports at the top of the file (PEP 8). Use it only for genuinely heavy libraries where startup time matters, not for standard library or lightweight packages.

### Generator/Iterator Patterns

Process large datasets one item at a time instead of loading everything into a list.

```python
# Bad: loads all lines into memory
lines = open("huge.log").readlines()
for line in lines:
    process(line)

# Good: processes one line at a time
with open("huge.log") as f:
    for line in f:
        process(line)
```

### Performance Linting

Enable performance rules in ruff:

```toml
[tool.ruff.lint]
select = ["E", "F", "PERF", "C4"]
```

`PERF` catches unnecessary list copies, redundant iterations, and other common Python performance mistakes. `C4` catches unnecessary comprehensions.

### Threading and the GIL

Python's GIL (Global Interpreter Lock) means only one thread can execute Python code at a time. But this does **not** mean threads are useless:

- **I/O-bound work** (network calls, file reads, database queries): threads help, because the GIL is released while waiting for I/O.
- **CPU-bound Python code** (pure loops, string processing): threads do not help. Use `multiprocessing` instead.
- **CPU-bound C extensions** (numpy, Pillow, torch): threads often help, because these libraries release the GIL during computation.

For most vibe coding projects (web apps, API clients, data pipelines), the bottleneck is I/O, so `threading.Thread` or `concurrent.futures.ThreadPoolExecutor` works fine.

### Memory Leaks

A memory leak in Python usually means a list, dict, or set that grows forever and is never cleaned up. The program works fine for hours, then slows down and eventually crashes.

Common pattern:

```python
# Bad: grows forever in a long-running server
all_requests = []
def handle_request(req):
    all_requests.append(req)  # never cleaned up
```

If you collect data over time (logs, metrics, history), set a maximum size or clean up periodically.

### Performance Checklist

- [ ] `PERF` and `C4` linting rules enabled
- [ ] `functools.lru_cache` used where applicable
- [ ] No string concatenation with `+=` in loops
- [ ] Generators used for large data processing
- [ ] `time.monotonic()` for duration measurements
