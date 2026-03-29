> [README](../../README.md) > [Docs](../) > **Performance**

# Performance

> **TL;DR** -- Measure before you optimize. The three causes of slowness: unnecessary work, missing limits, blocking waits. Set timeouts on all external calls. Add LIMIT to every query. Cache what is read often. Stream large data. For crash safety: write to temp file, then rename.

Performance is not optimization. It is thinking ahead so things are not unnecessarily slow. You do not need to make everything fast. You need to avoid making things accidentally slow.


## Why Vibe Coders Must Care

AI writes code that works. But "works" and "works well" are different things. A database query that returns results in 50ms with 10 rows can take 30 seconds with 10,000 rows. A download function that loads an entire file into memory works until someone uploads a 2GB video.

You do not need to optimize everything. But you need to know the three things that make software slow: **unnecessary work**, **missing limits**, and **blocking waits**. Most performance problems fall into one of these categories.


## Measure Before You Optimize

This is the most important rule. Do not guess where the bottleneck is. Measure.

Why? Because the bottleneck is almost never where you think. Developers routinely optimize the wrong thing, making code more complex without making it faster. This is the equivalent of "diagnose before you treat" in medicine.

```text
start = monotonic_clock()
result = do_expensive_thing()
duration = monotonic_clock() - start
log("Operation took {duration} seconds")
```

Use a monotonic clock, not wall-clock time. Why? Because wall-clock time can jump backward (clock adjustments, NTP sync). A monotonic clock always moves forward.

Add timing to any operation you suspect is slow. The number tells you where to focus.


## When Your Project Is Slow: Where to Start

If your project is slow and you do not know why, follow this path:

1. **Identify what is slow.** Add timing (see above) to the main operations. Is it the database query? The API call? The data processing? You need a number, not a feeling.

2. **Check the database first.** Most slowness in typical apps comes from missing indexes, N+1 queries, or fetching too much data. See the [Database Performance](#database-performance) section.

3. **Check external calls.** Network calls to APIs, file downloads, LLM calls: these are orders of magnitude slower than local operations. See the [Network and I/O](#network-and-io) section.

4. **Check for unnecessary work.** Are you computing the same result multiple times? Loading data you do not use? See [Caching](#caching) and [Do Not Fetch What You Do Not Need](#do-not-fetch-what-you-do-not-need).

5. **If it is still slow**, consider whether the operation should happen in the background instead of making the user wait. See [Synchronous vs. Asynchronous](#synchronous-vs-asynchronous-architecture).

> "My project is slow but I do not know where the bottleneck is. Add timing measurements to the main operations: database queries, API calls, file operations, and data processing. Log each with its duration in seconds. Then tell me which operations take the longest."


## Understand What Is Expensive

Not all operations cost the same. This table shows rough orders of magnitude:

| Operation | Approximate time | Relative cost |
|---|---|---|
| In-memory operation (L1 cache) | 1 ns | 1x |
| In-memory operation (hash map lookup) | 50-200 ns | 100x |
| Disk read (SSD) | 100 us | 100,000x |
| Network call (same datacenter) | 1-5 ms | 1,000,000x |
| Network call (internet) | 50-200 ms | 100,000,000x |
| LLM API call | 1-30 s | 1,000,000,000x |

These are approximations, not measurements. The key insight: **a network call is roughly a million times slower than looking something up in memory.** If you put a network call inside a loop that runs 100 times, you turned a fast operation into a multi-second wait.

**Latency vs. Throughput:** These are two different things that beginners often confuse. Latency is how long a single request takes (like travel time). Throughput is how many requests you can handle per second (like lane capacity). A six-lane highway (high throughput) does not help if you are stuck in traffic (high latency). Solving latency problems is different from solving throughput problems.


## The Fundamentals

### Do Not Fetch What You Do Not Need

Every database query should include a `LIMIT` and an `ORDER BY`. Every API call should request only the fields you use. Why? Because without limits, your code works fine during development (10 rows) and breaks in production (10,000 rows).

`ORDER BY` matters because without it, `LIMIT` returns whichever rows the database finds first, which can be different each time. This leads to bugs that are hard to reproduce.

```sql
Bad:  SELECT * FROM users
Good: SELECT name, email FROM users WHERE active = 1 ORDER BY created_at DESC LIMIT 50
```

### Set Timeouts on Everything External

Every network call, every database query, every subprocess: set a timeout. Why? Because without a timeout, a single slow or unresponsive service can hang your entire application forever.

```text
// Bad: hangs forever if the server does not respond
http_get("https://api.example.com/data")

// Good: fails after 10 seconds
http_get("https://api.example.com/data", timeout = 10)
```

Make timeouts configurable so you can adjust them without changing code.

### Caching

Caching means storing a result so you do not have to compute or fetch it again.

> Think of it like writing down a phone number instead of calling directory assistance every time. The note is your cache. It is instant to read, but it might become outdated if the number changes.

**When to cache:** When data is read often but changes rarely. An API response that changes once a day. A database query result used on every page load. A computed value that takes 2 seconds to calculate.

**When NOT to cache:** When data changes constantly (your cache is always outdated). When data is different for every request (nothing to reuse). When correctness matters more than speed (financial transactions, real-time systems).

**The hardest problem: cache invalidation.** When do you throw away the note and call directory assistance again? Options:

- **Time-based (TTL):** Cache expires after N seconds. Simple, but data can be stale until expiry.
- **Event-based:** Clear the cache when the underlying data changes. Precise, but requires knowing when data changes.
- **Manual:** Clear the cache when you deploy or update. Only for truly static data.

For language-specific caching tools, see your [language mapping](../languages/).

### Lazy Over Eager

Load data, models, and resources when needed, not at startup. Why? Because startup time matters for user experience, and resources you load but never use waste memory.

Patterns:
- Start background services on first request, not at boot
- Load ML models when the first job arrives, not when the server starts
- Use feature flags to skip initialization of disabled modules entirely
- For heavy library imports, use lazy loading (only when startup time is a real problem)

### Design for Expected Scale

Document in your project definition what scale you target. A tool for one user does not need connection pooling. A tool for 10,000 users does. Making the decision explicit prevents both over-engineering and under-engineering.


## Database Performance

### Indexing

Without indexes, the database reads every row to find what you asked for (full table scan). With indexes, it jumps directly to the matching rows.

> Think of it like the index at the back of a textbook. Without it, you flip through every page to find "photosynthesis." With it, you look up the keyword and jump to page 247. The downside: every time you add a page, the index must be updated too. More indexes is not always better.

```sql
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_status_created ON jobs(status, created_at);
```

Why a composite index (two columns)? Because if you often query `WHERE status = 'pending' ORDER BY created_at`, a single-column index on `status` still needs to sort. The composite index handles both filter and sort.

> "Review my database queries. For each query, check: is there an index that covers the WHERE and ORDER BY columns? Flag any query that would cause a full table scan on a table with more than 1000 rows. Suggest specific indexes."

### Avoid N+1 Queries

The N+1 problem: you fetch a list of items (1 query), then for each item you fetch related data (N queries). With 100 items, that is 101 queries instead of 2.

```text
// Bad: N+1. One query per user.
users = query("SELECT * FROM users LIMIT 100")
for each user in users:
    orders = query("SELECT * FROM orders WHERE user_id = ?", user.id)

// Good: 2 queries total. Fetch all related data in one query.
users = query("SELECT * FROM users LIMIT 100")
user_ids = collect ids from users
orders = query("SELECT * FROM orders WHERE user_id IN (?...)", user_ids)
```

If you use an ORM, look for "eager loading" options (e.g., `select_related`, `prefetch_related`, `include`, or `with`).

### Pagination

`LIMIT 50` gives you the first 50 results. But how do you get results 51-100? That is pagination.

**Offset-based** (simple, good enough for most projects):

```sql
SELECT * FROM posts ORDER BY created_at DESC LIMIT 50 OFFSET 50  -- page 2
```

Downside: with large offsets (page 1000), the database still reads and skips all previous rows.

**Cursor-based** (better for large datasets):

```sql
SELECT * FROM posts WHERE created_at < '2026-03-28' ORDER BY created_at DESC LIMIT 50
```

Use the last item's timestamp as the cursor for the next page. No skipping, consistent performance regardless of page number.

### SQLite Tuning

If you use SQLite, two settings make a significant difference:

```sql
PRAGMA journal_mode=WAL;      -- allows reading while writing
PRAGMA synchronous=NORMAL;    -- safe in WAL mode, faster than FULL
```

WAL (Write-Ahead Logging) lets multiple threads read the database while one thread writes. Without WAL, readers block writers and vice versa.

**Important caveats:**
- WAL does not enable multiple simultaneous writers. SQLite remains single-writer. Concurrent writes will still get "database is locked" errors under heavy load.
- `synchronous=NORMAL` is safe specifically because WAL is active. Without WAL, NORMAL can lose data on power failure.
- WAL does **not work on network filesystems** (NFS, SMB, shared Docker volumes). It can cause database corruption. Only use WAL with local storage.

### Connection Pooling

> Opening a database connection is like hailing a taxi: it takes time. A connection pool is like a taxi stand: a few taxis wait ready, and you just get in.

For SQLite, connection pooling is unnecessary because connections are cheap (just opening a local file). For PostgreSQL, MySQL, or remote databases, always use a connection pool. Without one, each request opens and closes a connection, which adds latency and can exhaust the database's connection limit under load.


## Network and I/O

### Streaming Large Data

Never load large files entirely into memory. Use streaming (chunked reading/writing). Why? Because a 2GB file in memory means 2GB of RAM, which can crash your program.

```text
// Bad: loads entire file into memory
data = http_get(url).body

// Good: streams in chunks
response = http_get(url, stream = true)
file = open(output_path)
for each chunk in response.chunks(size = 65536):
    file.write(chunk)
file.close()
```

### Retry with Exponential Backoff

When an external service fails, retry, but not immediately. Each retry waits longer. Why? Because if the service is overloaded, hammering it with retries makes the problem worse.

```text
delay = min(max_delay, base_delay * (2 ^ attempt))   // 1s, 2s, 4s, 8s...
delay += random(0, 1)                                 // jitter: prevent thundering herd
sleep(delay)
```

Why jitter? Without it, if 100 clients hit a failing service at the same time, all 100 retry at the exact same moment (after 1s, then after 2s, then after 4s). This is called "thundering herd" and it keeps the service down. Random jitter spreads the retries out.

Set a maximum number of retries and a maximum delay. Log each retry so you can see patterns.

### Batch Operations

If you need to send 100 notifications, do not make 100 separate API calls. Batch them.

```text
// Bad: 100 round trips
for each item in items:
    query("INSERT INTO log VALUES (?)", item)

// Good: 1 round trip
query_batch("INSERT INTO log VALUES (?)", items)
```

### Synchronous vs. Asynchronous Architecture

Sometimes the best performance improvement is not making code faster, but not making the user wait.

> A user uploads a video and you need to transcribe it. If you do it synchronously, the user waits 2 minutes staring at a spinner. If you do it asynchronously ("Your video is being processed, we will notify you"), the *perceived* performance is instant, even though the actual processing time is identical.

The fastest operation is the one nobody waits for. If an operation takes more than a few seconds, consider moving it to a background queue and notifying the user when it is done.


## Crash Recovery and Idempotency

What happens when your program crashes in the middle of an operation? Does it leave half-written files? Corrupt data? Lose work? These questions matter for any project that processes data, runs background jobs, or writes to disk.

### Idempotency: Safe to Run Twice

An operation is idempotent if running it twice produces the same result as running it once. Why this matters: if your program crashes after step 3 of 5 and restarts, it will run steps 1-3 again. If those steps are not idempotent, you get duplicate data, double charges, or corrupt files.

Practical patterns:

- **Check before you act.** Before processing a file, check if the output already exists and is valid. If it does, skip.
- **Write atomically.** Write to a temporary file first, then rename it to the final name. If the program crashes during writing, the temp file is incomplete but the old file is intact.
- **Use status flags.** Track "pending / running / done" for each job. On restart, reset "running" back to "pending" and reprocess.

```text
// Bad: overwrites output even if it already exists
function process(input_path, output_path):
    result = expensive_computation(input_path)
    write_file(output_path, result)

// Good: skip if output already exists (idempotent)
function process(input_path, output_path):
    if file_exists(output_path) and file_size(output_path) > 0:
        return                                // already processed
    result = expensive_computation(input_path)
    tmp = output_path + ".tmp"
    write_file(tmp, result)
    rename(tmp, output_path)                  // atomic on same filesystem
```

### Stale State on Restart

If your program tracks state (jobs in a database, tasks in a queue), crashes leave behind "running" entries that will never complete. On startup, reset stale state:

```sql
-- On startup: reset any jobs that were "running" back to "pending"
UPDATE jobs SET status = 'pending' WHERE status = 'running';
```

This is a one-line fix that prevents your program from getting permanently stuck after a crash.

> "Review my project for crash recovery issues. Check: what happens if the program crashes mid-operation? Are there half-written files, stale locks, or orphaned 'running' state? Are write operations atomic (temp file + rename)? Can the program restart safely without duplicating work?"


## Distributed Caching

The [Caching](#caching) section above covers the basics: store a result so you do not compute it twice. That works perfectly when your application runs on a single server. But what happens when you have two or three instances of your application running behind a load balancer? Each instance has its own local cache, which means:

- User A hits instance 1, which caches the result
- User B hits instance 2, which does not have the cache and recomputes
- User A updates the data on instance 1, which clears its local cache
- User B still sees the stale cached version on instance 2

The caches are out of sync because they do not know about each other.

### Shared Cache: One Cache for All Instances

The solution is a shared cache that all instances read from and write to. Think of it as moving from personal notebooks (each person writes their own notes) to a shared whiteboard (everyone reads and writes the same board).

Redis and Memcached are the two most common tools for this. They are key-value stores that sit between your application instances and your database:

```text
request -> instance 1 --\
request -> instance 2 ---+--> shared cache --> database
request -> instance 3 --/
```

All instances check the same cache. If instance 1 writes a value, instance 2 can read it immediately.

### Cache-Aside Pattern

The most common pattern for using a shared cache is cache-aside (also called "lazy population"):

```text
function get_user(user_id):
    // Step 1: check cache
    cached = cache.get("user:" + user_id)
    if cached is not null:
        return cached

    // Step 2: cache miss, query database
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)

    // Step 3: store in cache for next time
    cache.set("user:" + user_id, user, ttl = 300)    // expires in 5 minutes
    return user
```

Why cache-aside? Because the application controls what gets cached and when. The cache only stores data that is actually requested, not everything in the database. And if the cache goes down, the application still works (just slower, because every request hits the database).

### Cache Stampede

A subtle problem: your cache entry for a popular item expires, and 500 requests arrive at the same moment. All 500 see the cache miss. All 500 query the database simultaneously. This is a cache stampede, and it can bring your database to its knees.

> Think of it like a cafeteria that runs out of coffee. If one person starts brewing a new pot, everyone waits. But if there is no coordination, 50 people all try to brew their own pot at the same time, and the kitchen burns down.

Two common solutions:

**Locking:** The first request that sees a cache miss acquires a lock. All other requests wait briefly, then read the freshly populated cache.

```text
function get_popular_item(item_id):
    cached = cache.get("item:" + item_id)
    if cached is not null:
        return cached

    lock_acquired = cache.acquire_lock("lock:item:" + item_id, timeout = 5)
    if lock_acquired:
        // I won the lock, I will refresh the cache
        item = database.query("SELECT * FROM items WHERE id = ?", item_id)
        cache.set("item:" + item_id, item, ttl = 300)
        cache.release_lock("lock:item:" + item_id)
        return item
    else:
        // Someone else is refreshing, wait and retry
        sleep(0.1)
        return get_popular_item(item_id)    // retry, cache should be warm now
```

**Stale-while-revalidate:** Serve the expired value while one request refreshes the cache in the background. Users see slightly stale data for a few seconds, but the database is never overwhelmed.

### When NOT to Distribute

If your application runs on a single server, a shared cache adds complexity for no benefit. Local in-memory caching is faster (no network hop to the cache server), simpler (no extra service to run), and sufficient.

Distribute your cache only when you have multiple application instances that need to share state. Start with local caching. Move to distributed caching when you actually deploy multiple instances.

> "My application runs on multiple instances behind a load balancer. Review my caching strategy. Am I using local caches that could get out of sync between instances? Suggest where I should use a shared cache (like Redis) and where local caching is still fine. Identify any risk of cache stampede on popular data."


## Database Query Planning

Indexes tell the database what to look up quickly. But how do you know if the database is actually using your index? That is where query plans come in.

### What Is a Query Plan?

When you send a query to the database, it does not just run it blindly. It first creates a plan: "How should I find this data?" The plan considers which indexes exist, how many rows are in each table, and which approach would be fastest.

> Think of it like planning a route before driving. You could take the highway (fast but indirect) or side streets (short but slow). The GPS evaluates both and picks one. The query plan is the database's GPS.

You can see the plan by putting `EXPLAIN` in front of your query:

```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 42 ORDER BY created_at DESC LIMIT 10;
```

### How to Read a Query Plan

Query plans vary by database, but the key things to look for are:

- **Sequential scan (Seq Scan / Full Table Scan):** The database reads every row in the table. On a table with 100 rows, this is fine. On a table with 1,000,000 rows, this is a problem.
- **Index scan:** The database uses an index to jump directly to the matching rows. This is what you want for large tables.
- **Sort:** The database sorts results in memory. If you see a sort step on a large result set, a composite index that includes the ORDER BY column could eliminate it.
- **Nested loop:** For joins, the database loops through one table and looks up matching rows in the other. Fine for small tables, expensive for large ones.

```sql
-- Example output (simplified, varies by database):
-- Seq Scan on orders       <- bad on large tables: reads every row
--   Filter: customer_id = 42

-- vs.

-- Index Scan using idx_orders_customer on orders   <- good: uses index
--   Index Cond: customer_id = 42
```

### Common Query Plan Problems

**Missing index:** The most common problem. The database does a sequential scan because no index covers your WHERE clause. Solution: add an index on the filtered column (see [Indexing](#indexing)).

**Wrong join order:** When joining multiple tables, the database picks an order. Sometimes it picks wrong, especially with outdated statistics. If a join query is slow, check which table the plan scans first.

**Outdated statistics:** The database keeps statistics about table sizes and value distribution to make planning decisions. After large data imports or deletes, these statistics can be wrong. Most databases update them automatically, but you can force a refresh:

```sql
-- PostgreSQL
ANALYZE orders;

-- MySQL
ANALYZE TABLE orders;

-- SQLite (rebuilds statistics automatically, but you can force it)
ANALYZE;
```

### When to Worry About Query Plans

Do not run EXPLAIN on every query. Focus on:

- Queries on tables with more than 10,000 rows
- Any query that takes more than 100ms
- Queries that run frequently (every page load, every API call)
- Queries that suddenly became slow (table grew, statistics outdated)

For small tables (under 1,000 rows), a sequential scan is often faster than an index scan because the overhead of using the index exceeds the cost of reading a few pages. The database knows this. Trust it for small tables.

> "Run EXPLAIN on my slowest database queries. For each query plan, tell me: is it using a sequential scan on a large table? Is there a sort step that could be eliminated with a composite index? Are there nested loops on large tables? Suggest specific indexes or query rewrites to improve the plan."


## Profiling Complex Systems

Measuring individual operations (as described in [Measure Before You Optimize](#measure-before-you-optimize)) works well for simple programs. But what about a system where a request touches an API endpoint, calls two services, queries a database, hits a cache, and returns? Where is the time going?

### Flame Graphs: Seeing Where Time Goes

A flame graph is a visual representation of where your program spends its time. The x-axis is time, and each horizontal bar is a function call. The wider the bar, the more time that function takes. Bars are stacked to show the call hierarchy: the function at the bottom called the one above it, which called the one above that.

> Think of it like an X-ray of your program's execution. Instead of guessing "the database is slow," you can see exactly which function call accounts for 60% of the total time.

```text
|-- handle_request (100%)  ----------------------------------|
    |-- authenticate (5%)  --|
    |-- fetch_user_data (70%)  --------------------------------|
        |-- db_query (45%)  ----------------------|
        |-- serialize (25%)  --------------|
    |-- render_response (25%)  --------------|
```

In this example, you can see immediately: `db_query` inside `fetch_user_data` is the bottleneck. Optimizing `authenticate` (5%) would be a waste of time.

Most languages have profiling tools that generate flame graphs. See your [language mapping](../languages/) for specifics.

### Distributed Tracing: Following a Request Across Services

When your system has multiple services (a frontend, an API, a worker, a database), a single user request passes through several of them. Distributed tracing assigns a unique ID to each request and tracks it across all services:

```text
Request abc-123:
  [API Gateway]     2ms    |--|
  [Auth Service]    15ms      |---------------|
  [Order Service]   45ms                       |---------------------------------------------|
    [Database]      30ms                          |------------------------------|
    [Cache lookup]  2ms                                                           |--|
  [Response]        3ms                                                                |--|
Total: 67ms
```

Without distributed tracing, each service only knows its own timing. You see "the API takes 67ms" but cannot tell that 30ms of that is a database query inside the order service.

The concept is simple: generate a trace ID at the entry point, pass it along with every internal call, and log timing with that ID at each step. Tracing tools then reassemble the full picture.

### The 80/20 Rule of Profiling

Profile first, optimize the biggest bottleneck, repeat. This is the most efficient approach because performance improvements compound:

1. Profile the system and find the top bottleneck
2. Optimize that one thing
3. Profile again (the bottleneck may have shifted)
4. Repeat until performance is acceptable

Why not optimize everything at once? Because after fixing the biggest bottleneck, the second-biggest bottleneck might no longer matter (it might now represent only 5% of total time). Profiling after each change tells you where the next dollar of effort buys the most improvement.

### Common Profiling Mistakes

**Profiling with tiny data.** Your development database has 50 rows. Production has 500,000. A query that takes 1ms on 50 rows can take 5 seconds on 500,000 rows. Always profile with realistic data volumes, or at minimum, test with 10x your current production data.

**Optimizing the wrong layer.** You spend a week optimizing your serialization code (25% of request time) when the database query (45%) is the real bottleneck. Profile first, then decide what to optimize.

**Profiling only in development.** Development machines are different from production: different hardware, different network latency, different load. A function that is fast on your local machine with one concurrent user can be slow in production with 100 concurrent users. If possible, profile in a staging environment that mirrors production.

**Measuring averages instead of percentiles.** If 99% of your requests take 50ms and 1% take 10 seconds, the average is 150ms, which looks fine. But 1% of your users have a terrible experience. Look at the 95th percentile (p95) and 99th percentile (p99), not just the average.

> "Profile my application and identify the top 3 bottlenecks by time spent. For each bottleneck, tell me: what percentage of total time does it account for? What causes it (slow query, network call, heavy computation)? What is the simplest fix? Start with the biggest bottleneck."


## Language-Specific Performance

For language-specific performance patterns (caching decorators, string handling, lazy imports, concurrency models, memory management), see your [language mapping](../languages/). Example: [Python](../languages/python.md#performance-patterns).


## Advanced: Concurrency and Resource Management

> These patterns are for projects that do multiple things simultaneously (web servers, background workers, multi-threaded pipelines). If your project is a simple script or CLI tool, you probably do not need this section yet.

### Cooperative Cancellation

When a long-running operation needs to be cancelled (user abort, shutdown), do not kill the thread. Set a flag and check it at defined points. Why? Because killing threads leaves resources in undefined states (open files, locked databases, half-written data).

```text
cancel_flag = new shared flag (initially false)

function long_running_task():
    for each segment in process_large_file(path):
        if cancel_flag is set:
            cleanup()
            return
        handle(segment)

// To cancel from another thread:
cancel_flag.set()
```

### Resource Lifecycle (Load, Use, Unload)

Expensive resources (ML models, GPU memory, database connections) should have a clear lifecycle: load when needed, keep warm while in use, unload after an idle timeout. This prevents both wasted memory (never unloading) and slow responses (loading every time).

A simple pattern: track the last-used time. A background thread periodically checks if the resource has been idle longer than its TTL (time-to-live). If yes, unload it.

### Semaphores for Exclusive Resources

Some resources can only be used by one operation at a time (a GPU model, a serial port, a file being written). Use a semaphore (a lock that controls how many operations can access a resource simultaneously) to control access.

```text
gpu_lock = new semaphore(max = 1)    // only 1 concurrent user

function run_inference(data):
    acquire gpu_lock:
        return model.predict(data)
    release gpu_lock
```

### Graceful Shutdown

When your program needs to stop, give running operations time to finish. Why? Because abrupt termination can corrupt data, leave locks in place, or lose work in progress.

Pattern: signal all threads to stop, wait a defined timeout (e.g., 5 seconds), then force-terminate anything still running.


## Performance Review Prompts

**Important:** AI reviews catch obvious patterns (missing limits, N+1 queries) but miss subtle issues (cache invalidation bugs, race conditions under load). Always measure actual performance with realistic data volumes.

### Quick Check

> "Review my project for performance issues. Check: all database queries have LIMIT and ORDER BY, no expensive operations inside loops, all external calls have timeouts, large data uses streaming instead of loading into memory. Report findings. Do not fix automatically."

### Full Review

> "Read my AGENTS.md and review the codebase for performance issues. Check: database queries have appropriate indexes, no N+1 query patterns, all external calls have configurable timeouts, large data processed via streaming or pagination, resources cleaned up after use, retry logic uses exponential backoff with jitter, caching used where data is read often but changes rarely. Report findings sorted by impact."

### Database-Specific

> "Review all database queries in this project. For each query: does it have a LIMIT and ORDER BY? Would it benefit from an index? Is it called inside a loop (N+1 risk)? Does it fetch columns that are not used? Suggest specific indexes and query improvements."


## Checklist

This covers the most common performance issues. It is not exhaustive.

### General

- [ ] Expected scale documented in project definition
- [ ] Performance measured, not guessed (timing on critical operations)
- [ ] All external calls have configurable timeouts
- [ ] No full-data fetches where partial would suffice
- [ ] Expensive operations not inside loops (network calls, DB queries)
- [ ] Large data uses streaming or pagination
- [ ] Retry logic uses exponential backoff with jitter
- [ ] Caching used for frequently read, rarely changed data

### Database

- [ ] Indexes on frequently filtered/sorted columns
- [ ] No N+1 query patterns
- [ ] All queries have LIMIT and ORDER BY where appropriate
- [ ] Pagination for user-facing data lists
- [ ] SQLite: WAL mode enabled on local storage (if applicable)

### Resources

- [ ] Heavy resources loaded lazily (on first use, not at startup)
- [ ] Long-lived resources unloaded after idle timeout
- [ ] Graceful shutdown with timeout for running operations
- [ ] No unbounded growth in lists/dicts/sets (memory leak prevention)

### Language-Specific

See your [language mapping](../languages/) for language-specific performance checks (e.g., [Python](../languages/python.md#performance-checklist)).


---

See also: [Stage 1: Start](../start.md) for the basics, [Stage 3: Enforce](../enforce.md) for when to add automated checks, [Security](security.md) for the other cross-cutting concern.
