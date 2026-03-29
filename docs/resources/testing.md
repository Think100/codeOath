> [README](../../README.md) > [Docs](../) > **Testing**

# Testing

> **TL;DR (practical guide)** -- Let AI write tests, you review expected results, then AI implements to pass them. Test domain logic first (fast, no dependencies). Use fakes (in-memory implementations) instead of mocks for ports. Run the full test suite after every AI-generated change to catch regressions. For language-specific tools and syntax, see [languages/python.md](../languages/python.md).

How testing works, what to test, and how to use tests to steer your AI.


## How Testing Works

Every test follows the same cycle:

1. **Define** what you want to test (one specific behavior)
2. **State the expected result** (what should happen)
3. **Run the test** (let the computer check)
4. **Pass or fail** (the result is binary, no "maybe")
5. **Act on the result** (fix the code if it fails, move on if it passes)

A single test looks like this:

```
test calculate_discount_applies_percentage:
    result = calculate_discount(100, percent = 10)
    expect result == 90

test calculate_discount_rejects_negative:
    expect error when calculate_discount(100, percent = -5)
```

The first test defines a behavior (10% discount on 100), states the expected result (90), and the framework checks it. If the function returns 89, the test fails. You know exactly what broke and where.

This is the entire concept. Everything else is just applying this cycle to different parts of your code.


## Let Your AI Write Tests, Then Implement

Nobody writes 500 tests by hand. Your AI writes the tests. Your job is to review them and make sure they test the right things.

**The two-step pattern:**

1. Tell your AI to write tests for a feature (it generates the tests)
2. Review the tests: do they cover the important cases? Then tell the AI to make them pass

This works because tests are easy to read and verify. You do not need to know how to write test code. You just need to look at the expected results and ask: "Is that what I want?" If the test says `expect discount(100, 10) == 90`, you can tell whether 90 is correct.

> "Read my AGENTS.md. Write tests for the invoice calculation: test normal cases, zero values, negative amounts, and boundary conditions. Show me the tests before writing the implementation."

Review the tests. Remove ones that test the wrong thing. Add cases you care about in plain language ("also test what happens when tax rate is over 100%"). Then:

> "Good. Now write the implementation that makes all tests pass."

**Why this is so effective:** the AI now has a concrete, verifiable target. It can iterate until all tests pass without asking you clarifying questions. And if it changes something later that breaks a test, you see it immediately.

This idea comes from Test-Driven Development (TDD). The classic version says the developer writes tests first. With AI, the same principle works, but the AI writes both the tests and the implementation. You steer and verify.

```
// Your AI generates this:
test user_cannot_order_more_than_stock:
    product = create_product(name = "Widget", stock = 5)
    expect error when place_order(product, quantity = 10)

// You review it: yes, that is the behavior I want.
// Then: "Make this test pass. The function should be in domain/orders."
```


## What to Test

### Domain Logic (Unit Tests)

Start here. Domain code has no external dependencies (no database, no API, no file system), which makes tests fast, simple, and reliable. Just input and output.

**What to cover:**
- Core calculations and rules
- Boundary conditions (zero, negative, empty, maximum)
- Error cases (invalid input should be rejected, not silently accepted)

```
test invoice_total_with_tax:
    invoice = create_invoice(subtotal = 100, tax_rate = 0.19)
    expect invoice.total == 119

test invoice_rejects_negative_amount:
    expect error when create_invoice(subtotal = -50, tax_rate = 0.19)

test invoice_handles_zero_tax:
    invoice = create_invoice(subtotal = 100, tax_rate = 0)
    expect invoice.total == 100
```

### Security Concerns

Security is not a separate test category. It is a concern that runs through your regular tests. You add security-relevant assertions to your unit and integration tests.

**What to check:**
- Bad input is rejected at the boundary (adapter layer), not passed to domain logic
- Error responses do not leak internal details (no stack traces, no database names, no file paths)
- Secrets do not appear in responses or logs
- Authentication is enforced where required

```
test api_rejects_path_traversal:
    response = request("/download/../../etc/passwd")
    expect response.status == 400

test error_response_hides_internals:
    response = request("/api/broken-endpoint")
    expect "stack trace" not in response.body
    expect "password" not in response.body
    expect "database" not in response.body
```

**SQL injection:** The correct defense is parameterized queries (prepared statements), not input filtering. If your adapter uses parameterized queries, injection is structurally impossible. Test that your adapter uses them, not that a specific attack string fails:

```
test search_with_injection_string_returns_empty:
    results = search_users("'; DROP TABLE users; --")
    expect results == []
    // The table must still exist and be queryable
    expect search_users("Alice") != null
```

For the full security checklist, see [security.md](security.md).

### Adapters (Integration Tests)

Test adapters when they do something non-trivial: complex queries, data transformations, error handling at boundaries. Simple adapters that just pass data through do not need their own tests.

Integration tests use real infrastructure (a real database, a real API). They are slower than unit tests and need more setup, but they verify that your code actually works with the outside world.

**When to add them:** when you have adapters worth testing. Not on day one, but not "never" either. If your adapter builds SQL queries, transforms API responses, or handles connection failures, it needs tests.


## Testing Without Real Infrastructure

This is the payoff from separating domain and adapters ([grow.md](../grow.md), Concept 3). Define a port (interface) in your domain, then create a **fake** (a simplified, in-memory implementation) for testing.

```
// The port: what the domain needs (defined in domain/)
interface InvoiceStore:
    save(invoice) -> void
    find(id) -> Invoice or null

// The fake: a test double that works without a database
class InMemoryInvoiceStore implements InvoiceStore:
    storage = {}

    save(invoice):
        storage[invoice.id] = invoice

    find(id):
        return storage.get(id) or null
```

A fake is a type of **test double**: a stand-in for a real dependency. It has a working implementation but takes a shortcut (dictionary instead of database). Unlike a mock, it does not verify how it was called. It just works.

Use the fake in a test:

```
test invoice_service_saves_and_retrieves:
    store = new InMemoryInvoiceStore()
    service = new InvoiceService(store)

    service.create_invoice(id = "INV-1", subtotal = 100, tax = 0.19)
    invoice = service.get_invoice("INV-1")

    expect invoice.total == 119
```

No database needed. The test runs in milliseconds. If it passes, the domain logic is correct regardless of which database adapter you use in production.

**Limitation:** a fake does not verify that the real adapter works. It only verifies that domain logic is correct *assuming* the adapter fulfills the interface. You still need integration tests for the real adapter when it does non-trivial work.


## Regression Tests for AI-Assisted Development

When your AI modifies existing code, the highest risk is breaking something that used to work. This is called a **regression**: a behavior that was correct and is now broken.

Run your full test suite after every AI-generated change. This is not optional. It is the primary defense against silent regressions. A test that passed yesterday and fails today tells you exactly what the AI broke.

This is also why writing tests first (see above) compounds in value: every test you write becomes a permanent guard against future regressions.


## Static Analysis (Linting, Type Checking, Formatting)

These are not tests. They do not run your code. They read it and flag problems based on patterns.

**Linter** (e.g., ruff for Python, eslint for JavaScript): catches common mistakes, unused imports, style violations, and some security issues. Think of it as a spell-checker for code.

**Type checker** (e.g., mypy for Python, tsc for TypeScript): checks that you are not passing a string where a number is expected. Catches bugs before you run the code.

**Formatter** (e.g., ruff format, prettier): makes code look consistent. No tabs-vs-spaces debates. The formatter decides.

A perfectly formatted function that returns the wrong result will pass all static analysis and fail the unit test. They catch different classes of problems.

> "Set up linting, type checking, and formatting for this project. Use the standard tools for my language. Make sure they run with a single command and can be added to pre-commit hooks later."

For Python-specific tools and configuration, see [languages/python.md](../languages/python.md).


## How They Work Together

| Check | What it catches | When it runs | Speed |
|---|---|---|---|
| Unit tests | Wrong behavior, broken logic | Every change, in CI | Seconds |
| Integration tests | Adapter bugs, infrastructure issues | On demand, in CI | Seconds to minutes |
| Linter | Code smells, common bugs, style | Before every commit | Instant |
| Type checker | Type mismatches | Before every commit | Seconds |
| Formatter | Inconsistent style | Before every commit | Instant |

Security assertions are part of your unit and integration tests, not a separate step.

Start with unit tests for your domain logic and a linter. Add integration tests when you have non-trivial adapters. Add pre-commit hooks when you want automation ([enforce.md](../enforce.md)).


---

See also: [Stage 2: Grow](../grow.md) for when to start testing, [Stage 3: Enforce](../enforce.md) for automating checks with pre-commit hooks and CI.
