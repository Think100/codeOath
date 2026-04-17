> [README](../../README.md) > [Docs](../) > **Rust Language Mapping**

# Rust Language Mapping

> **TL;DR** -- Stage 1: flat Cargo project, `clippy` + `cargo test`. Stage 2: split the code into a `domain/` module (business logic) and `adapters/` module (database, CLI, etc.), wired together in `main.rs`. Stage 3: promote each layer to its own crate inside a Cargo workspace — the compiler now rejects forbidden imports by itself. Rust-specific extras this guide covers: typed errors with `thiserror`/`anyhow`, `#![forbid(unsafe_code)]`, dependency scanning with `cargo audit` and `cargo deny`.

This file translates codeOath concepts into Rust. If you read [start.md](../start.md) or [grow.md](../grow.md) and wondered "what does that look like in Rust?", this is the answer.

You do not need to read this file front to back. Jump to the stage you are in.


## Concept Mapping

codeOath uses generic terms. Here is what they mean in Rust:

| codeOath Concept        | Rust Implementation                                       | When |
|-------------------------|-----------------------------------------------------------|------|
| Source folder           | `src/` with `main.rs` (binary) or `lib.rs` (library)      | Stage 1+ |
| Build config            | `Cargo.toml`                                              | Stage 1+ |
| Tests                   | `#[cfg(test)] mod tests` in source, `tests/` for integration | Stage 1+ |
| Linter                  | `cargo clippy -- -D warnings`                             | Stage 1+ |
| Formatter               | `cargo fmt`                                               | Stage 1+ |
| Dependency management   | `cargo` with `Cargo.lock` committed for binaries          | Stage 1+ |
| Type checker            | The compiler itself, `cargo check`                        | Stage 1+ |
| Port / Interface        | `trait` in `domain/ports.rs`                              | Stage 2+ |
| Immutable domain object | Plain `struct` with no `&mut self` methods                | Stage 2+ |
| Boundary validation     | `serde` with `#[serde(deny_unknown_fields)]` in adapters  | Stage 2+ |
| Composition root        | `main.rs`, explicit wiring                                | Stage 2+ |
| Import enforcement      | Cargo workspace: separate crates, compiler rejects cross-layer imports | Stage 3 |
| Dependency vulnerability | `cargo audit`                                            | Stage 3 |
| License / source policy | `cargo deny`                                              | Stage 3 |
| Secret scanner          | `gitleaks` (language-agnostic, pre-commit hook)           | Stage 3 |
| Error handling          | `Result<T, E>`, `thiserror` for libs, `anyhow` for apps   | All |
| Async pattern           | `tokio`, `async`/`await`                                  | When needed |

You do not need everything from this table on day one. Start with Stage 1 tools, add the rest when you move to Stage 2 or 3.


## Folder Structure by Stage

### Stage 1: Single crate, flat

Everything in one crate. No layers, no separation. Good enough for small projects.

```text
myproject/
├── docs/
│   └── todo.md
├── src/
│   └── main.rs
├── tests/
│   └── integration_test.rs
├── .gitignore
├── Cargo.toml
├── AGENTS.md
└── README.md
```

Minimal `.gitignore` for Rust projects:

```text
# build artifacts
/target

# editor backups
**/*.rs.bk

# secrets
.env
config/.env
```

Commit `Cargo.lock` for binaries (reproducible builds). Do not commit `Cargo.lock` for libraries published to crates.io (downstream users pin their own versions).

Minimal `Cargo.toml`:

```toml
[package]
name = "myproject"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"

[dependencies]

[dev-dependencies]
```

To run your project and tests:

```bash
cargo run                   # run the project
cargo test                  # run tests
cargo clippy -- -D warnings # lint, fail on warnings
cargo fmt                   # format
```

### Configuration

Keep all settings in one place. Do not scatter `std::env::var()` calls across your code. In [grow.md](../grow.md), `config/` is where settings live. In Rust, a plain struct works well for this.

Define your settings in `config/.env` (never committed to git):

```text
DB_PATH=/data/app.sqlite
API_URL=https://api.example.com
MAX_RETRIES=3
DEBUG=false
```

Load them into a struct:

```rust
// config/settings.rs
use std::path::PathBuf;

pub struct AppConfig {
    pub db_path: PathBuf,
    pub api_url: String,
    pub max_retries: u32,
    pub debug: bool,
}

impl AppConfig {
    pub fn from_env() -> anyhow::Result<Self> {
        Ok(Self {
            db_path: std::env::var("DB_PATH")?.into(),
            api_url: std::env::var("API_URL")?,
            max_retries: std::env::var("MAX_RETRIES")
                .unwrap_or_else(|_| "3".into())
                .parse()?,
            debug: std::env::var("DEBUG")
                .unwrap_or_else(|_| "false".into())
                .eq_ignore_ascii_case("true"),
        })
    }
}
```

Call `AppConfig::from_env()` once in `main.rs` and pass the result to whatever needs it. Domain code never reads environment variables directly; it receives values as parameters.

For more complex configuration (multiple sources, layered overrides), use the `figment` or `config` crate.

### Stage 2: Domain and adapters separated

Your core logic (`domain/`) is now separate from everything that talks to the outside world (`adapters/`). Why? Because your AI sees clear boundaries: in `domain/`, no database imports allowed. You can test your logic without a real database. You can swap SQLite for PostgreSQL without touching your logic. See [domain-and-adapters.md](../resources/domain-and-adapters.md) for the full explanation.

```text
myproject/
├── docs/
│   ├── todo.md
│   └── decisions.md
├── src/
│   ├── main.rs
│   ├── lib.rs
│   ├── domain/
│   │   ├── mod.rs
│   │   ├── models.rs
│   │   ├── ports.rs
│   │   └── services.rs
│   └── adapters/
│       ├── mod.rs
│       ├── cli.rs
│       └── db.rs
├── tests/
│   └── integration_test.rs
├── .gitignore
├── Cargo.toml
├── AGENTS.md
└── README.md
```

`lib.rs` declares the modules and re-exports the public API. `main.rs` is the binary entry point that wires everything together.

**Note:** At Stage 2, the domain/adapters rule is discipline. The compiler does not stop `domain/models.rs` from writing `use crate::adapters::db;`. That enforcement arrives in Stage 3.

---

**You can stop here.** Stage 1 and 2 cover most Rust projects. Everything below (workspaces, error strategy, security and performance patterns) is reference material for when you need it.

---

### Stage 3: Workspace with enforced boundaries

A Rust **workspace** is a set of related crates (packages) in one repository that share a build. Stage 3 promotes each Stage 2 layer to its own crate: `domain` and `adapters` become separate crates, and a new `app` crate holds `main.rs`. Why? Each crate declares its dependencies explicitly in its own `Cargo.toml`. When `domain`'s `Cargo.toml` does not list `adapters` as a dependency, importing from `adapters` inside `domain` fails to compile — the boundary is enforced by the compiler, not by a linter or convention. Stronger than Python's `import-linter`, which runs as a post-hoc check.

```text
myproject/
├── Cargo.toml                  (workspace manifest)
├── crates/
│   ├── domain/
│   │   ├── Cargo.toml          (no dependency on adapters)
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── models.rs
│   │       ├── ports.rs
│   │       └── services.rs
│   ├── adapters/
│   │   ├── Cargo.toml          (depends on domain)
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── db.rs
│   │       └── cli.rs
│   └── app/
│       ├── Cargo.toml          (depends on domain and adapters)
│       └── src/
│           └── main.rs
├── docs/
│   ├── todo.md
│   ├── decisions.md
│   └── definition.md
├── .gitignore
├── AGENTS.md
└── README.md
```

Workspace `Cargo.toml`:

```toml
[workspace]
resolver = "3"
members = ["crates/domain", "crates/adapters", "crates/app"]

[workspace.package]
edition = "2024"
rust-version = "1.85"
version = "0.1.0"

[workspace.dependencies]
thiserror = "2"
anyhow = "1"
myproject-domain = { path = "crates/domain" }
```

Declaring shared dependencies once at the workspace level (and referencing them via `foo.workspace = true` below) keeps versions in sync across crates and avoids accidental duplicates.

`crates/domain/Cargo.toml`:

```toml
[package]
name = "myproject-domain"
edition.workspace = true
version.workspace = true

[dependencies]
thiserror.workspace = true
```

`crates/adapters/Cargo.toml`:

```toml
[package]
name = "myproject-adapters"
edition.workspace = true
version.workspace = true

[dependencies]
myproject-domain.workspace = true
# database, http, etc.
```

The domain crate has no knowledge of adapters. Adapter code importing from domain is allowed and expected; the other direction will not compile.


## Trait Example

Ports are how your domain says "I need something from the outside world" without knowing who provides it. In Rust, you define them as `trait`s.

The domain defines the contract:

```rust
// domain/ports.rs
use crate::domain::models::Order;

pub trait OrderRepository {
    fn find_by_id(&self, order_id: &str) -> Result<Option<Order>, RepositoryError>;
    fn save(&self, order: &Order) -> Result<(), RepositoryError>;
}

#[derive(Debug, thiserror::Error)]
pub enum RepositoryError {
    #[error("order not found: {0}")]
    NotFound(String),
    #[error("backend failure: {0}")]
    Backend(String),
}
```

If you plan to share the repository across threads (web handlers, worker pools), declare the trait with thread-safety bounds: `pub trait OrderRepository: Send + Sync`.

An adapter implements the contract:

```rust
// adapters/db.rs
use std::sync::Mutex;

use crate::domain::models::Order;
use crate::domain::ports::{OrderRepository, RepositoryError};

pub struct SqliteOrderRepository {
    conn: Mutex<rusqlite::Connection>,
}

impl SqliteOrderRepository {
    pub fn new(conn: rusqlite::Connection) -> Self {
        Self { conn: Mutex::new(conn) }
    }
}

impl OrderRepository for SqliteOrderRepository {
    fn find_by_id(&self, order_id: &str) -> Result<Option<Order>, RepositoryError> {
        // SELECT FROM orders WHERE id = ?
        todo!()
    }

    fn save(&self, order: &Order) -> Result<(), RepositoryError> {
        // INSERT INTO orders ...
        todo!()
    }
}
```

**Note:** This example is synchronous. For an async driver like `sqlx`, use `async fn` in the trait (Rust 1.75+); the `async-trait` crate is still needed for `Box<dyn OrderRepository>` dynamic dispatch.

The composition root (`main.rs`) wires them together. This is the only place that knows about both domain and adapters:

```rust
// main.rs
use myproject::adapters::db::SqliteOrderRepository;
use myproject::domain::services::OrderService;

fn main() -> anyhow::Result<()> {
    let conn = rusqlite::Connection::open("orders.db")?;
    let repo = SqliteOrderRepository::new(conn);
    let service = OrderService::new(repo);
    // wiring done; in a real program, call service methods here
    // (e.g. service.process_pending_orders()?).
    let _ = service;
    Ok(())
}
```

The domain service is generic over the trait, not tied to SQLite:

```rust
// domain/services.rs
use crate::domain::ports::OrderRepository;

pub struct OrderService<R: OrderRepository> {
    repo: R,
}

impl<R: OrderRepository> OrderService<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }
    // ...
}
```


## Testing

For general test strategy (what to test, how to use tests to steer your AI), see [testing.md](../resources/testing.md). This section covers the Rust-specific mechanics.

Rust places unit tests inside the source file in a `#[cfg(test)] mod tests { ... }` block. They can access private items. Integration tests live in `tests/` at the project root and only see the public API. Both run with `cargo test`.

```rust
// src/domain/services.rs
pub fn total(prices: &[u64]) -> u64 {
    prices.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sums_prices() {
        assert_eq!(total(&[10, 20, 30]), 60);
    }
}
```

**Faking a port in tests** -- no mocking library required. Write a struct that implements the trait with whatever behavior the test needs:

```rust
use std::sync::Mutex;
use crate::domain::models::Order;
use crate::domain::ports::{OrderRepository, RepositoryError};

struct FakeOrderRepository {
    stored: Mutex<Vec<Order>>,
}

impl OrderRepository for FakeOrderRepository {
    fn find_by_id(&self, _id: &str) -> Result<Option<Order>, RepositoryError> {
        Ok(None)
    }
    fn save(&self, order: &Order) -> Result<(), RepositoryError> {
        self.stored.lock().unwrap().push(order.clone());
        Ok(())
    }
}
```

For traits with many methods, the `mockall` crate generates fakes from the trait definition.

For larger test suites, `cargo install cargo-nextest` gives you a faster test runner with clearer failure output. It runs each test in its own process, which also catches state that leaks between tests.


## Import Enforcement (Stage 3)

A workspace crate can only use items from crates listed in its `[dependencies]`. If `domain`'s `Cargo.toml` does not list `adapters`, the line

```rust
use myproject_adapters::db::SqliteOrderRepository;
```

inside `domain` fails to compile. No extra tooling, no CI check.

Related tools:

- `cargo-modules`: visualize the module and crate graph (spot unintended coupling before it compiles).
- `cargo-deny`: enforce licenses, banned crates, and duplicate-version policies.
- `cargo-machete`: find unused dependencies.


## Pre-Commit Hooks

Automated checks that run before each `git commit`. If a check fails, the commit is blocked. The `pre-commit` tool itself comes from the Python ecosystem but works across languages. Install once (`pip install pre-commit && pre-commit install`), then every commit is checked automatically.

Rust tools are not published as pre-commit mirrors, so Rust checks run as local hooks using your installed toolchain:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: cargo-fmt
        name: cargo fmt
        entry: cargo fmt --all --
        language: system
        types: [rust]
        pass_filenames: false
      - id: cargo-clippy
        name: cargo clippy
        entry: cargo clippy --all-targets -- -D warnings
        language: system
        types: [rust]
        pass_filenames: false
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

What each hook does:

- **cargo fmt**: makes your code look consistent (indentation, spacing, line breaks)
- **cargo clippy**: finds common mistakes and bad habits in your Rust code. The `-D warnings` flag blocks the commit on any warning, not just errors.
- **gitleaks**: catches passwords or API keys accidentally written into the code before they enter Git

For general CI/CD context and the relationship between pre-commit and GitHub Actions, see [build-pipeline.md](../resources/build-pipeline.md).


## Error Handling Strategy

Rust has two dominant error-handling crates. Pick one per crate type:

- **Library crates (including `domain`)**: use `thiserror`. Define a typed error enum per module. Callers can pattern-match specific variants.
- **Binary crates (`app`, `main.rs`)**: use `anyhow::Result`. Ergonomic propagation with `?`, good default `Display` for logs. No need for callers to pattern-match.

**Why?** `anyhow::Error` erases the concrete type, which is fine for top-level reporting but bad for domain logic that needs to react to specific failure modes. `thiserror` keeps types precise but is verbose in glue code where you only want to bubble errors up.

```rust
// domain uses thiserror
#[derive(Debug, thiserror::Error)]
pub enum OrderError {
    #[error("invalid state transition: {from} -> {to}")]
    InvalidTransition { from: String, to: String },
    #[error(transparent)]
    Repository(#[from] RepositoryError),
}

// main uses anyhow
fn main() -> anyhow::Result<()> {
    let service = build_service()?;
    service.run().context("while running the order service")?;
    Ok(())
}
```

Avoid `Box<dyn Error>` in new code. It works but has none of the ergonomics of either pattern.

**Watch out:** Never use `.unwrap()` or `.expect()` in production code paths. They panic on error, which aborts the binary. Reserve them for tests and for genuine invariant violations (unreachable branches, static resources that must exist).


## Common Pitfalls

### Memory that never gets freed

Rust normally cleans up memory automatically when a value goes out of scope. But if you build a data structure where two objects point at each other (think: a tree where each child also has a pointer back to its parent), neither of them can ever be cleaned up. Rust does not detect this at compile time, so the program runs fine but leaks memory slowly.

**When to watch for it:** any graph-like structure with back-references, such as trees with parent pointers, observer patterns, or doubly-linked lists. The common fix is to make the "back" direction a weak reference, so it does not count toward ownership and the cycle can be broken.

### Async code that refuses to compile across threads

Async functions in Rust produce values (futures) that can sometimes be moved between threads and sometimes not. The default Tokio runtime uses multiple threads, so it requires values that can be moved. If you accidentally hold on to something that cannot, the compiler refuses to build your code with a cryptic message about `Send` bounds.

The classic cause is holding a lock across an `.await` point: the task pauses, the lock stays alive, and now the whole future cannot travel to another thread. The fix is usually small: drop the lock before the `.await`, or switch to a thread-safe equivalent of whatever you were holding.

### Channels that grow forever

Channels in Rust come in two flavours: bounded (fixed capacity) and unbounded (no limit). Unbounded channels feel attractive because the producer never has to wait. But if the producer is faster than the consumer, the queue grows until the process runs out of memory and dies.

Default to bounded channels. When the channel is full, the producer has to wait, and this is called backpressure. It is a feature, not a bug: it tells you that the consumer cannot keep up, before the whole system falls over.


## Security Patterns

These patterns address Rust-specific security concerns. For general security principles (input validation, authentication, OWASP), see [security.md](../resources/security.md). For review prompts that catch common AI mistakes (hidden errors, scope drift, hardcoded secrets), see [ai-code-review.md](../resources/ai-code-review.md).

### Forbid `unsafe` by Default

Add this to `lib.rs` or `main.rs`:

```rust
#![forbid(unsafe_code)]
```

The compiler rejects any `unsafe` block in the crate. If you genuinely need `unsafe` (FFI, performance primitives), use `#![deny(unsafe_code)]` and allow it per-module with `#[allow(unsafe_code)]` plus a comment explaining why.

### Deserialization

Always opt into strict deserialization when parsing untrusted input:

```rust
#[derive(serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ApiRequest {
    pub user_id: String,
    pub amount: u64,
}
```

Without `deny_unknown_fields`, extra fields are silently ignored, which hides typos and can mask injection attempts that rely on field confusion.

**Watch out:** Never deserialize untrusted `bincode`, `rmp-serde`, or other binary formats without size limits. Malicious input can request multi-gigabyte allocations and DoS the process. In `bincode` 2.x use `config::standard().with_limit::<N>()` (const-generic byte limit), or validate sizes before decoding.

### Command Execution

When calling external commands, pass arguments as a list. Never concatenate into a shell string:

```rust
// Bad: shell injection risk
std::process::Command::new("sh")
    .arg("-c")
    .arg(format!("convert {}", user_filename))
    .status()?;

// Good: no shell, no injection
std::process::Command::new("convert")
    .arg(user_filename)
    .status()?;
```

### Constant-Time Comparisons

When comparing secrets (tokens, API keys, MACs), use the `subtle` crate:

```rust
use subtle::ConstantTimeEq;

if expected.len() == provided.len()
    && expected.as_bytes().ct_eq(provided.as_bytes()).into()
{
    // token matches
}
```

**Why?** Regular `==` short-circuits on the first mismatched byte, leaking timing information that attackers can use to guess secrets one byte at a time. `ct_eq` requires equal-length slices; a length mismatch is checked separately, which leaks the length (usually fine) but never the contents.

### Cryptographic Randomness

For long-lived secrets (keys, stored tokens), use `rand::rngs::OsRng` or the `getrandom` crate. From `rand` 0.9 onward, `rand::rng()` (formerly `thread_rng()`) is OS-seeded and periodically reseeded, so it is acceptable for short-lived values like per-request session IDs. When in doubt, use `OsRng`. The overhead is negligible for secret generation.

### Dependency Auditing

```bash
cargo install cargo-audit cargo-deny
cargo audit                 # known CVEs in dependencies
cargo deny check            # licenses, bans, duplicates, advisories
```

Add both to CI. `cargo deny` also catches duplicate versions of the same crate, which can hide subtle bugs and bloat binaries.

### Secret Scanning

`gitleaks` as a pre-commit hook. Language-agnostic, catches AWS keys, JWTs, private keys, and custom patterns.


## Performance Patterns

These patterns address Rust-specific performance concerns. For general performance principles (caching strategy, database optimization, crash recovery): [performance.md](../resources/performance.md).

### Release Profile

Debug builds are 10-100x slower than release builds. Always measure with `cargo build --release`. For production binaries, tune the release profile:

```toml
[profile.release]
lto = true              # link-time optimization, smaller and faster binaries
codegen-units = 1       # better optimization, slower compile
strip = true            # remove debug symbols from the binary
panic = "abort"         # smaller binary, faster panics, no unwinding
```

**Watch out:** `panic = "abort"` removes the ability to catch panics with `catch_unwind`. Only set it if you do not rely on panic recovery.

### Prefer Iterators Over Manual Loops

The compiler usually generates equivalent code for both. The reason to prefer iterators is readability and fewer off-by-one bugs, not performance:

```rust
// Idiomatic, clear intent
let total: u64 = orders.iter().map(|o| o.amount).sum();

// Manual loop, harder to read, index arithmetic is a bug vector
let mut total = 0u64;
for i in 0..orders.len() {
    total += orders[i].amount;
}
```

### One-Time Initialization

Use `std::sync::LazyLock` (stable since 1.80) for expensive values that should be computed once:

```rust
use std::sync::LazyLock;
use regex::Regex;

static EMAIL_RE: LazyLock<Regex> = LazyLock::new(|| {
    // Panic here is an invariant check: a static regex literal must compile,
    // otherwise the program is fundamentally broken and should abort at startup.
    Regex::new(r"^[^@]+@[^@]+$").expect("static email regex must compile")
});
```

Before 1.80, `once_cell::sync::Lazy` served the same role.

### Avoid Unnecessary Clones

`.clone()` is explicit but easy to overuse. In hot paths, prefer borrowing (`&T`), `Cow<'_, T>` for maybe-owned data, or `Arc<T>` for shared ownership across threads.

```rust
// Bad: clones the whole string for every call
fn greet(name: String) { println!("hello {name}"); }

// Good: borrows, no allocation
fn greet(name: &str) { println!("hello {name}"); }
```

Clippy lints like `clippy::redundant_clone` and `clippy::clone_on_copy` catch common cases.

### Benchmarking

Use `criterion` for statistical benchmarks:

```toml
[dev-dependencies]
criterion = "0.5"

[[bench]]
name = "my_bench"
harness = false
```

Criterion runs many iterations, detects regressions, and produces HTML reports. Plain `#[bench]` requires nightly and gives weaker results.

### Allocation Profiling

For allocation-heavy workloads, profile with `dhat`:

```toml
[dev-dependencies]
dhat = "0.3"
```

This tells you where allocations happen and how long they live, which often beats CPU profiling for Rust code where the hot spots are in `malloc` and `free`.

### Async Runtime Choice

`tokio` is the default for networked services. For CPU-bound work, do not reach for async: it helps with I/O concurrency, not with parallelism. Use `rayon` for parallel CPU work.

### Performance Checklist

- [ ] `clippy` pedantic and perf lints enabled where noise is tolerable
- [ ] Measurements taken with `--release`
- [ ] `LazyLock` or `OnceLock` for one-time init
- [ ] No `.clone()` in hot paths without a comment explaining why
- [ ] `criterion` benches for anything performance-sensitive
- [ ] Release profile tuned (`lto`, `codegen-units`, `strip`)
