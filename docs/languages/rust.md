> [README](../../README.md) > [Docs](../) > **Rust Language Mapping**

# Rust Language Mapping

> **TL;DR** -- Stage 1: `Cargo.toml` + `clippy` + `cargo test`. Stage 2: `domain/` module with `trait` ports, `adapters/` with implementations, plain `struct` for models, `main.rs` wires them. Stage 3: Cargo workspace with `domain` and `adapters` as separate crates -- imports are enforced by the compiler, not by a linter. Errors: `thiserror` in domain/libs, `anyhow` in binaries. Security: `#![forbid(unsafe_code)]`, `serde(deny_unknown_fields)`, `cargo audit` and `cargo deny`.

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
| Async pattern           | `tokio` or `async-std`, `async`/`await`                   | When needed |

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

[profile.release]
lto = true
codegen-units = 1
strip = true
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

At Stage 2, the domain/adapters rule is discipline: the compiler does not stop `domain/models.rs` from writing `use crate::adapters::db;`. That enforcement arrives in Stage 3.

---

**You can stop here.** Stage 1 and 2 cover most Rust projects. Everything below (workspaces, error strategy, security and performance patterns) is reference material for when you need it.

---

### Stage 3: Workspace with enforced boundaries

Same conceptual structure as Stage 2, but each layer is a separate crate inside a Cargo workspace. The compiler enforces layer boundaries: if `domain` does not list `adapters` as a dependency, importing from adapters inside domain is a compile error, not a lint warning. This is stronger enforcement than Python's `import-linter`.

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
resolver = "2"
members = ["crates/domain", "crates/adapters", "crates/app"]

[workspace.package]
edition = "2024"
rust-version = "1.85"
version = "0.1.0"
```

`crates/domain/Cargo.toml`:

```toml
[package]
name = "myproject-domain"
edition.workspace = true
version.workspace = true

[dependencies]
thiserror = "2"
```

`crates/adapters/Cargo.toml`:

```toml
[package]
name = "myproject-adapters"
edition.workspace = true
version.workspace = true

[dependencies]
myproject-domain = { path = "../domain" }
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

The trait is synchronous, so this example uses `rusqlite` (sync). If you need an async database driver like `sqlx`, the trait methods have to become `async fn` too (Rust 1.75+ supports native async in traits; before that, the `async-trait` crate).

The composition root (`main.rs`) wires them together. This is the only place that knows about both domain and adapters:

```rust
// main.rs
use myproject::adapters::db::SqliteOrderRepository;
use myproject::domain::services::OrderService;

fn main() -> anyhow::Result<()> {
    let conn = rusqlite::Connection::open("orders.db")?;
    let repo = SqliteOrderRepository::new(conn);
    let service = OrderService::new(repo);
    service.run()?;
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


## Import Enforcement (Stage 3)

In Python, import enforcement is a post-hoc lint. In Rust, it is part of the build. A workspace crate can only use items from crates listed in its `[dependencies]`. If `domain`'s `Cargo.toml` does not list `adapters`, the line

```rust
use myproject_adapters::db::SqliteOrderRepository;
```

inside `domain` will fail to compile with a clear error. No extra tooling needed, no CI check to configure.

Related tools for deeper control:

- `cargo-modules`: visualize the module and crate graph (useful for spotting unintended coupling before it compiles).
- `cargo-deny`: enforce licenses, banned crates, and duplicate-version policies across the workspace.
- `cargo-machete`: find unused dependencies.


## Error Handling Strategy

Rust has two dominant error-handling crates. Pick one per crate type:

- **Library crates (including `domain`)**: use `thiserror`. Define a typed error enum per module. Callers can pattern-match specific variants.
- **Binary crates (`app`, `main.rs`)**: use `anyhow::Result`. Ergonomic propagation with `?`, good default `Display` for logs. No need for callers to pattern-match.

Why not one or the other everywhere? `anyhow::Error` erases the concrete type, which is fine for top-level reporting but bad for domain logic that needs to react to specific failure modes. `thiserror` keeps types precise but is verbose in glue code where you only want to bubble errors up.

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

Never use `.unwrap()` or `.expect()` in production code paths. They panic on error, which usually means the binary aborts. Reserve them for tests and for situations where a panic is genuinely the right response (invariant violation, unreachable branch).


## Security Patterns

These patterns address Rust-specific security concerns. For general security principles (input validation, authentication, OWASP): [security.md](../resources/security.md).

### Forbid `unsafe` by Default

Add this to `lib.rs` or `main.rs`:

```rust
#![forbid(unsafe_code)]
```

This makes the compiler reject any `unsafe` block in the crate. If you genuinely need `unsafe` (FFI, performance primitives), use `#![deny(unsafe_code)]` instead and allow it only in specific modules with `#[allow(unsafe_code)]`, with a comment explaining why.

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

Never deserialize untrusted `bincode`, `rmp-serde`, or other binary formats without size limits. Malicious input can request multi-gigabyte allocations and DoS the process. Use `bincode`'s `Configuration::with_limit()` or validate sizes before decoding.

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

if expected.ct_eq(provided).into() {
    // token matches
}
```

Regular `==` short-circuits on the first mismatched byte, leaking timing information that attackers can use to guess secrets one byte at a time.

### Cryptographic Randomness

Use `rand::rngs::OsRng` or the `getrandom` crate for security-sensitive randomness (tokens, session IDs, keys). Never use the default `rand::thread_rng()` for secrets without confirming it is backed by the OS entropy source.

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

Debug builds are 10-100x slower than release builds. Always measure performance with `cargo build --release` or `cargo run --release`. For production binaries, tune the release profile:

```toml
[profile.release]
lto = true              # link-time optimization, smaller and faster binaries
codegen-units = 1       # better optimization, slower compile
strip = true            # remove debug symbols from the binary
panic = "abort"         # smaller binary, faster panics, no unwinding
```

`panic = "abort"` removes the ability to catch panics with `catch_unwind`. Only set it if you do not rely on panic recovery.

### Prefer Iterators Over Manual Loops

The compiler optimizes iterator chains aggressively, often vectorizing them. Manual indexed loops can block those optimizations:

```rust
// Idiomatic, optimizes well
let total: u64 = orders.iter().map(|o| o.amount).sum();

// Manual loop, usually slower and harder to read
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

`tokio` is the default for networked services. `async-std` has smaller mindshare now. For CPU-bound work, do not reach for async: it helps with I/O concurrency, not with parallelism. Use `rayon` for parallel CPU work.

### Performance Checklist

- [ ] `clippy` pedantic and perf lints enabled where noise is tolerable
- [ ] Measurements taken with `--release`
- [ ] `LazyLock` or `OnceLock` for one-time init
- [ ] No `.clone()` in hot paths without a comment explaining why
- [ ] `criterion` benches for anything performance-sensitive
- [ ] Release profile tuned (`lto`, `codegen-units`, `strip`)
