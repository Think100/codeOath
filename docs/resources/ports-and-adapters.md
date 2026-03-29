> [README](../../README.md) > [Docs](../) > **Ports and Adapters**

# Ports and Adapters

> **TL;DR (deep dive)** -- Domain defines what it needs (ports as abstract interfaces). Adapters provide the concrete implementation (database, API, UI). Dependencies always point inward: adapters know domain, domain knows nothing about adapters. The composition root (`main`) wires them together. Domain errors and infrastructure errors stay separate. Read [grow.md](../grow.md) first for the practical guide.

This document explains the architecture pattern that codeOath recommends from Stage 2 onward. It is language-neutral. See [languages/python.md](../languages/python.md) for concrete Python syntax. For the full background, see [Hexagonal architecture on Wikipedia](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)).

> The pseudocode below uses OOP-style notation (`class`, `implements`, `new`) for broad readability. If your language uses traits (Rust), implicit interfaces (Go), or functions instead of classes, the same principles apply with different syntax.


## The Core Idea

Separate your business logic from everything that connects it to the outside world.

- **Domain**: the rules, the logic, the core of what your software does
- **Adapters**: everything that connects the domain to external systems (database, API, UI, file system, bot, email)
- **Ports**: the contracts between domain and adapters

The domain defines what it needs (as abstract interfaces). Adapters provide the concrete implementation. The domain never knows which adapter is plugged in.


## Ports

A port is an abstract interface at the boundary of the domain. It describes a capability without specifying how it works.

There are two kinds:

**Outgoing ports** (domain needs something from outside):

```text
// Defined in domain. Implemented by an adapter.
interface DocumentStore {
    save_invoice(invoice: Invoice) -> void
    find_invoice(id: string) -> Invoice | null
}
```

**Incoming ports** (outside wants something from domain):

```text
// Defined in domain. Called by an adapter.
interface ImportInvoice {
    execute(raw_text: string) -> Result
}
```

Incoming ports define what the outside world can ask your domain to do. Outgoing ports define what your domain needs from the outside world. The use case is the class or function that *implements* an incoming port, not the port itself.


## Adapters

An adapter is a concrete implementation of a port.

**Outgoing adapter** (implements what domain needs):

```text
// Implements DocumentStore with SQL
class SqlDocumentStore implements DocumentStore {
    save_invoice(invoice: Invoice) -> void {
        // INSERT INTO invoices ...
    }
    find_invoice(id: string) -> Invoice | null {
        // SELECT FROM invoices WHERE id = ...
    }
}
```

**Incoming adapter** (translates external requests into use case calls):

```text
// HTTP endpoint that calls the use case
function handle_import_request(request) {
    raw_text = request.body
    result = import_invoice.execute(raw_text)
    return response(result)
}
```


## The Composition Root

The composition root is the single place where concrete adapters are created and wired to the domain. Nothing else in the project creates database connections or initializes external services.

```text
// main: the only place that knows all concrete types
store = new SqlDocumentStore(db_connection)
use_case = new ImportInvoice(store)
http_server = new HttpServer(use_case)
http_server.start()
```

Notice what is happening: `ImportInvoice` receives its `store` as a parameter instead of creating it or importing it directly. This is called **dependency injection** -- a fancy name for a simple idea: pass what you need in from outside instead of reaching for it yourself. Why? Because now you can pass in a different store (a test store, a different database) without changing the domain code. The composition root is the one place that decides which adapter fulfills which port.


## The Dependency Rule

Dependencies always point inward. The domain never imports from adapters.

| Element | May know about | Must not know about |
|---------|---------------|---------------------|
| domain/ | only domain types | frameworks, DB, HTTP, filesystem |
| domain/ports | domain types | concrete adapter implementations |
| adapters/ | ports, domain types | other adapters (in general) |
| main | everything | should not contain business logic |

The key insight: the domain defines what it needs (port), the adapter provides it, and main wires them together. The domain code compiles and can be tested without any adapter present.


## Errors Across the Boundary

When your adapter calls a database and the database is down, where should that error be handled? The rule: **domain errors and infrastructure errors are different things.**

- **Domain errors** (invalid invoice, negative amount, missing required field) are part of your business logic. The domain knows about these and returns them as results or raises domain-specific errors.
- **Infrastructure errors** (database unreachable, network timeout, file not found) are adapter problems. The adapter catches these and translates them into something the domain can understand, or lets them bubble up to the caller.

The domain should never see a `DatabaseConnectionError` or `HttpTimeoutError`. It should see "could not save the invoice" or "storage unavailable". The adapter translates infrastructure errors into domain language.

```text
// In the adapter: translate infrastructure errors
class SqlDocumentStore implements DocumentStore {
    find_invoice(id: string) -> Invoice | null {
        try {
            // SELECT FROM invoices WHERE id = ...
        } catch (DatabaseError) {
            throw StorageUnavailableError("cannot reach database")
        }
    }
}
```

`StorageUnavailableError` is a domain-level error. It does not mention SQL, connection pools, or network details. The domain code can handle it without knowing what database is behind it.


## Why This Matters for AI-Assisted Development

When your AI agent works in the domain folder:
- It cannot import database drivers (the linter prevents it at Stage 3)
- It sees only the port interface, not the concrete implementation
- It cannot accidentally couple business logic to infrastructure
- Tests work without mocking external systems (inject a test adapter)

When your AI agent works in an adapter:
- It knows exactly which port it must implement
- It cannot accidentally add business logic (that belongs in domain)
- Replacing the adapter (SQLite to PostgreSQL, REST to GraphQL) does not touch domain code


## When This Is Overkill

For projects with fewer than five files that take less than a week: do not use this. Keep everything flat. See [Stage 1](../start.md).

The rule of thumb: if your project has business logic worth protecting from infrastructure coupling, use ports and adapters. If it is a simple script or utility, skip it.


## Stage 3: What Changes

Everything above describes Stage 2: two layers (domain + adapters), ports in a single file (e.g., `domain/ports`), the composition root in `main`. This is enough for most small-to-medium projects.

When your use cases grow complex enough to need their own orchestration, Stage 3 introduces an **application layer** between domain and adapters. Use case implementations (like `ImportInvoiceHandler`) move from domain/ to application/. The incoming port interfaces stay in domain/. The domain stays pure logic.

```text
adapters/
├── in/              incoming (CLI, HTTP, bot, scheduler)
└── out/             outgoing (DB, email, APIs, filesystem)
application/         use cases, orchestration
domain/              pure logic, ports
main.*               composition root
```

The dependency rule extends to three layers:

| Element | May know about | Must not know about |
|---------|---------------|---------------------|
| domain/ | only domain types | frameworks, DB, HTTP, filesystem |
| domain/ports | domain types | concrete adapter implementations |
| application/ | domain, ports | concrete adapters directly |
| adapters/ | ports, domain types | other adapters (in general) |
| main | everything | should not contain business logic |

Import enforcement tooling turns these rules into automated checks that fail the build if violated. This is the wall that makes "structure is governance" real.

Do not jump to Stage 3 structure preemptively. See [triggers.md](triggers.md) for when it is time, and [enforce.md](../enforce.md) for the full menu of Stage 3 additions.


## Common Mistakes

These are things that go wrong often, especially in AI-assisted projects. If you recognize one, it is not a disaster. Just fix it.

**Database code in the middle of a calculation.** Your function calculates a price and halfway through it queries the database for the tax rate. Move the query out. Pass the tax rate in as a parameter. The calculation belongs in domain/, the database call in adapters/.

**Business logic in the adapter.** Your API endpoint validates the input, applies discount rules, checks inventory, and then saves the order. The discount rules and inventory check are business logic. They belong in domain/, not in the HTTP handler.

**One giant interface for everything.** Your `DatabasePort` has 20 methods because every database operation goes through one interface. Split it. A function that only reads invoices should receive a `ReadInvoices` interface, not the entire database.

**Adapters that know each other.** Your email adapter imports from your database adapter to look up the recipient. Adapters should not talk to each other directly. If email needs a recipient, the use case (or domain logic) should look it up and pass it in.

**Logic in the composition root.** Your `main` file decides which discount tier applies before wiring the dependencies. The composition root creates objects and connects them. It does not make business decisions.

**Catching everything with try/except pass.** Your AI wraps a block in a try-catch that silently swallows all errors. Now the code never crashes, but it also never tells you when something goes wrong. Catch specific errors, handle them explicitly, and let unexpected errors surface.

**Infrastructure errors leaking into domain code.** Your domain function catches `psycopg2.OperationalError` or `requests.ConnectionError`. Now the domain depends on a specific database driver or HTTP library. Let the adapter catch these and translate them into domain-level errors.

**Skipping ports because "it is just a small project."** You wire the database directly into domain code because adding an interface feels like overhead. Then you want to test the logic, and you need a running database. Even a one-method interface saves you from this.
