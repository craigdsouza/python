# 30-Day Python Developer Exam Prep Plan

Modern Python stack: backend (FastAPI, Django, SQLAlchemy, async), frontend integration (Jinja2, HTMX, Streamlit), databases, testing, and deployment.

---

## How to Use This Plan

- Each day has a **concept block** (read/watch), a **concept anchor** (CS fundamentals), and a **coding challenge**.
- Challenges are rated: `[Easy]` `[Medium]` `[Hard]` `[Expert]`
- Difficulty ramps gradually — Week 1 is foundations, Week 4 is production-grade.
- Time budget: ~2–3 hours/day.

---

## Week 1 — Modern Python Foundations

### Day 1 — Type Hints & Pydantic
**Concepts:** `typing` module, `Annotated`, `TypeVar`, Pydantic v2 models, validators, `model_dump()`

**Concept anchor:** Python is dynamically typed — variables have no declared type and the interpreter figures it out at runtime. Type hints and Pydantic add explicit contracts, catching bad data at the boundary of your system rather than deep inside it where bugs are harder to trace. The broader CS idea is type safety: the more you can prove about your data before it runs, the fewer surprises at runtime.

**Challenge [Easy]:** Define a Pydantic `User` model with fields: `id: int`, `email: EmailStr`, `age: int` (must be 18–99), `role: Literal["admin", "user"]`. Write a function that accepts a raw dict, validates it, and returns the model or raises a `ValidationError`. Test with both valid and invalid inputs.

---

### Day 2 — Async Python
**Concepts:** `async`/`await`, `asyncio.gather`, `asyncio.create_task`, event loop, `asyncio.Queue`, avoiding blocking calls

**Concept anchor:** A single-threaded event loop handles concurrency by pausing tasks that are waiting on I/O (network, disk) and switching to other ready tasks — no extra threads needed. This is the key distinction between concurrency (doing many things by interleaving them) and parallelism (doing many things simultaneously on multiple CPU cores). Web servers are I/O-bound — most time is spent waiting for responses, not computing — which makes async a natural fit.

**Challenge [Easy]:** Write an async function `fetch_all(urls: list[str])` that uses `asyncio.gather` with `asyncio.sleep` as a mock for HTTP delay (random 0.1–0.5s per URL). Print results in completion order and total elapsed time. Show why sequential would be slower.

---

### Day 3 — Decorators & Context Managers
**Concepts:** `functools.wraps`, parametrized decorators, `__enter__`/`__exit__`, `contextlib.contextmanager`, class-based context managers

**Concept anchor:** A decorator is a higher-order function — it takes a function as input and returns a new function. Functions being usable as values (passed around, returned, stored in variables) is a foundational idea in functional programming. Context managers implement RAII (Resource Acquisition Is Initialization): resources like file handles and database connections are guaranteed to be released when a block exits, even if an exception occurs.

**Challenge [Medium]:** Build a `@retry(times=3, delay=0.5, exceptions=(ValueError,))` decorator that retries a function on specified exceptions. Also build a `timer()` context manager that logs elapsed time. Compose both on a flaky mock function.

---

### Day 4 — Iterators, Generators & dataclasses
**Concepts:** `__iter__`/`__next__`, generator expressions, `yield from`, `@dataclass`, `field()`, `__post_init__`, `slots=True`

**Concept anchor:** An iterator produces values one at a time on demand rather than computing and storing all of them upfront — this is lazy evaluation. For large datasets (a 10GB log file, for instance), lazy evaluation is the difference between crashing your machine and processing data line by line in constant memory. Generator pipelines compose this idea: data flows through a chain of transformations without any intermediate list ever being fully materialised.

**Challenge [Medium]:** Implement a `Paginator` dataclass that wraps a list and yields pages of `n` items as a generator. Add a `total_pages` property and make it iterable with `__iter__`. Then write a pipeline using generator chaining to: read lines → filter blanks → parse as CSV row → yield dicts.

---

### Day 5 — Testing with pytest
**Concepts:** `pytest` fixtures, `conftest.py`, parametrize, `pytest-mock`, `monkeypatch`, coverage, `pytest-asyncio`

**Concept anchor:** A unit test verifies a single piece of logic in isolation — external dependencies (databases, APIs) are replaced with controlled fakes called mocks or stubs. Isolation ensures a test failure tells you exactly which unit broke, rather than leaving you to guess which of ten dependencies misbehaved. The key tension in testing is the unit/integration trade-off: unit tests are fast and precise, integration tests catch the bugs that only appear when components interact.

**Challenge [Medium]:** Write a `Calculator` class with `add`, `divide` (raises `ZeroDivisionError`), and a `history` list. Write a full pytest suite: parametrized tests, a fixture that resets history, a mock for an external `log_operation(op)` call, and one async test using `pytest-asyncio`.

---

### Day 6 — Python Packaging & Project Structure
**Concepts:** `pyproject.toml`, `uv` / `pip-tools`, virtual environments, `__init__.py`, relative imports, `src/` layout

**Concept anchor:** Modularity means each file has a single clear responsibility, and other modules depend on its public interface rather than its internals — this is separation of concerns. A virtual environment is an isolated Python installation: it solves dependency hell (two projects needing different versions of the same library) by giving each project its own private package set. Dependency pinning ensures your code runs identically on every machine and in CI.

**Challenge [Easy]:** Scaffold a project with `src/myapp/` layout containing two modules. Add `pyproject.toml` with metadata and dependencies. Write a `cli.py` entry point using `argparse` that accepts `--name` and `--count` and prints a greeting N times. Install it in editable mode and run via `myapp`.

---

### Day 7 — Week 1 Review Challenge
**Concept anchor:** A data pipeline is a series of transformations where the output of one stage is the input of the next — a foundational pattern in CS. Generators make pipelines memory-efficient by passing one item at a time through the entire chain rather than materialising intermediate lists. The review challenge also surfaces the cost of integration: each component (argparse, Pydantic, asyncio, pytest) is simple alone but wiring them together is where design decisions matter.

**Challenge [Hard]:** Build a CLI tool `csvtool` that:
1. Reads a CSV file path from args
2. Validates each row with a Pydantic model (columns: `name`, `email`, `age`)
3. Uses a generator pipeline to filter invalid rows and collect errors
4. Outputs valid rows as JSON and a summary of errors
5. Has a `--async` flag that processes multiple files concurrently with `asyncio`
6. Full pytest suite with fixtures and parametrize

---

## Week 2 — FastAPI Backend

### Day 8 — FastAPI Basics
**Concepts:** Path/query/body params, `HTTPException`, response models, `status` codes, automatic OpenAPI docs (`/docs`)

**Concept anchor:** Every web request is a client asking a server for something — the HTTP protocol defines the vocabulary (GET, POST, DELETE, PATCH) and the response codes (200 OK, 404 Not Found, 422 Unprocessable Entity). REST is an architectural style that maps these verbs to CRUD operations on resources: GET reads, POST creates, PUT/PATCH updates, DELETE removes. A response model is a contract: it defines exactly what shape of data the server promises to return.

**Challenge [Easy]:** Build a FastAPI app with:
- `GET /items/{item_id}` — returns item or 404
- `POST /items` — accepts a Pydantic body, stores in-memory dict
- `GET /items?skip=0&limit=10` — paginated list
- Response model that excludes internal fields

---

### Day 9 — Dependency Injection & Middleware
**Concepts:** `Depends()`, dependency chaining, `yield` dependencies, `BaseHTTPMiddleware`, CORS, request timing middleware

**Concept anchor:** Dependency injection (DI) means a function declares what it needs and the framework provides it — instead of the function creating its own dependencies. This inverts control: the caller, not the callee, decides what implementation to supply. Middleware is a chain of responsibility pattern: each layer processes the incoming request, passes it forward to the next layer, then processes the outgoing response on the way back — timing, auth checks, and logging all fit naturally here.

**Challenge [Medium]:** Add to yesterday's app:
- A `get_current_user` dependency that reads a fake `X-Token` header (hardcoded valid tokens)
- Protect `POST /items` with it
- Add a request-timing middleware that logs method, path, and elapsed ms
- Add CORS middleware allowing `http://localhost:3000`

---

### Day 10 — Async FastAPI + Background Tasks
**Concepts:** `async def` routes, `BackgroundTasks`, `asyncio.sleep` vs `time.sleep` in async context, `lifespan` events

**Concept anchor:** When a slow operation runs inside a request handler, the client waits — and the server is blocked from handling other requests. Background tasks decouple the response from the work: the server acknowledges immediately, and the work happens in a separate execution context. This is the fundamental idea behind every job queue and task scheduler: separate the act of accepting work from the act of doing it.

**Challenge [Medium]:** Build a `POST /reports/generate` endpoint that:
- Immediately returns `{ "job_id": "uuid", "status": "queued" }`
- Runs report generation as a `BackgroundTask` (mock: sleep 2s, write result to a dict)
- Exposes `GET /reports/{job_id}` to poll status (`queued` → `done` → result)
- Uses `lifespan` to initialize and tear down a shared in-memory "database" dict

---

### Day 11 — SQLAlchemy 2.0 + Alembic
**Concepts:** Declarative models, `Session`, `select()`, relationships (`relationship()`), `joinedload`, Alembic migrations, `AsyncSession`

**Concept anchor:** A relational database organises data into tables with typed columns and enforces relationships (foreign keys) between them. ACID — Atomicity, Consistency, Isolation, Durability — are the guarantees a database makes: a transaction either fully completes or fully rolls back, never leaving data in a half-written state. Schema migrations are version control for your database structure — Alembic tracks what shape the schema is in and applies incremental changes without dropping data.

**Challenge [Medium]:** Define SQLAlchemy models `Author` and `Book` (one-to-many). Use Alembic to generate and apply a migration. Write CRUD functions: create author, add book, get all books by author (with joined load). Use SQLite for simplicity.

---

### Day 12 — FastAPI + Database Integration
**Concepts:** `get_db` dependency with `yield`, request-scoped sessions, async SQLAlchemy, connection pooling

**Concept anchor:** Opening a new database connection for every HTTP request is expensive — a connection pool keeps a fixed set of connections alive and lends them to requests on demand, similar to a car rental fleet. Request-scoped sessions mean the connection is checked back into the pool when the request ends, whether it succeeded or failed. The `yield` dependency pattern guarantees cleanup runs even when an exception is raised — the same RAII principle from Day 3 applied to database connections.

**Challenge [Hard]:** Wire Day 11's models into a FastAPI app:
- `POST /authors` + `GET /authors/{id}/books`
- `POST /authors/{id}/books`
- `DELETE /books/{id}` (cascade check)
- Use `AsyncSession` with `asyncpg` (or SQLite async driver)
- Dependency that provides a session per request and rolls back on exception

---

### Day 13 — Authentication: JWT + OAuth2
**Concepts:** `OAuth2PasswordBearer`, `python-jose` / `PyJWT`, hashing with `passlib`, token expiry, refresh tokens

**Concept anchor:** A cryptographic hash function is one-way — you verify a password by hashing what the user typed and comparing it to the stored hash, but you can never reverse the hash to recover the original. This is why password breaches expose hashes, not passwords directly. JWTs are stateless tokens: the server signs them with a secret key using a digital signature algorithm (HS256), so it can verify authenticity later without storing session state — the token itself is the proof.

**Challenge [Hard]:** Add auth to the books API:
- `POST /auth/register` — hash password with bcrypt, store user
- `POST /auth/login` — verify password, return `access_token` (JWT, 30min) + `refresh_token` (24h)
- `POST /auth/refresh` — exchange refresh token for new access token
- Protect all write endpoints; `GET` endpoints are public
- Return `401` on expired/invalid tokens

---

### Day 14 — Week 2 Review Challenge
**Concept anchor:** A production API is not one feature but many subsystems — auth, data persistence, background work, API contracts — each simple in isolation but composing into something complex. Combining subsystems introduces emergent behaviour: integration bugs that don't appear in any individual component's tests. The review challenge forces you to wire these together, which is where design decisions (session scope, error propagation, async boundaries) have real consequences.

**Challenge [Expert]:** Build a fully authenticated **Task Manager API**:
- Users register/login (JWT auth)
- CRUD for `Task` (`title`, `description`, `status: enum`, `due_date`, `owner_id`)
- `GET /tasks` filters by `status`, `due_before`, sorted by due date
- Background task: when a task is marked `done`, log completion time async
- Full pytest suite using `httpx.AsyncClient` as test client, SQLite in-memory DB fixture
- Alembic migrations included

---

## Week 3 — Databases, Caching & Advanced Backend

### Day 15 — PostgreSQL Deep Dive
**Concepts:** Indexes, `EXPLAIN ANALYZE`, transactions, isolation levels, `FOR UPDATE`, JSON columns, full-text search (`tsvector`)

**Concept anchor:** A database index is like a book's index — it trades extra write overhead for dramatically faster lookups by maintaining a sorted structure (typically a B-tree) separate from the table data. The query planner decides how to execute a query; `EXPLAIN ANALYZE` shows its reasoning and actual timing. Isolation levels and `SELECT FOR UPDATE` are how databases handle multiple users reading and writing the same rows concurrently without corrupting data — this is concurrency control, a core problem in systems that share mutable state.

**Challenge [Medium]:** Write raw SQL (via `asyncpg` or `psycopg3`) for:
1. A query using `tsvector` full-text search on a `posts` table
2. A transaction that transfers "credits" between two users with `SELECT FOR UPDATE` (no negative balances)
3. Add a `GIN` index and show the `EXPLAIN` output before/after

---

### Day 16 — Redis: Caching & Pub/Sub
**Concepts:** `redis-py` / `aioredis`, cache-aside pattern, TTL, `SETEX`, pub/sub, Redis as a job queue

**Concept anchor:** Caching works because of temporal locality — data accessed recently is likely to be accessed again soon. The cache-aside pattern (check cache first, fall back to DB on miss, write result to cache) keeps the primary database from being hammered by repeated identical reads. TTL (time-to-live) ensures stale data eventually expires — this is the fundamental tension in caching: the fresher the data, the more cache misses; the longer the TTL, the more stale reads.

**Challenge [Medium]:** Add to the books API:
- Cache `GET /authors/{id}/books` in Redis with 60s TTL; invalidate on write
- A `POST /notifications/publish` that publishes to a Redis channel
- A background subscriber that logs received messages
- Write a helper `@cached(ttl=60, key_fn=...)` decorator

---

### Day 17 — Celery & Task Queues
**Concepts:** Celery workers, brokers (Redis/RabbitMQ), `@shared_task`, `apply_async`, `chain`/`chord`/`group`, retries, task state

**Concept anchor:** A message queue decouples the producer (your web server) from the consumer (a worker process) — the producer drops a job on the queue and moves on immediately, while workers pick jobs up independently. This is the producer/consumer pattern: a foundational concurrency primitive. It also enables horizontal scaling — add more workers to process more jobs in parallel without changing the producer at all. Exponential backoff on retries prevents a failing external service from being hammered by rapid retries.

**Challenge [Hard]:** Build a Celery pipeline:
- Task 1: `download_data(url)` — mock fetch, return raw string
- Task 2: `process_data(raw)` — parse and return summary dict
- Task 3: `store_result(summary)` — write to a file
- Chain them: `download_data.s(url) | process_data.s() | store_result.s()`
- Add retry logic (3 attempts, exponential backoff) to Task 1
- Expose `POST /jobs` in FastAPI that fires the chain and returns a task ID

---

### Day 18 — WebSockets & SSE
**Concepts:** FastAPI `WebSocket`, connection manager pattern, Server-Sent Events, `StreamingResponse`

**Concept anchor:** HTTP is half-duplex — the client asks, the server answers, then the connection closes. WebSockets establish a persistent, full-duplex channel over TCP where either side can send a message at any time without waiting for a request. SSE is a lighter alternative: one-way server-to-client streaming over a long-lived HTTP connection. The difference matters architecturally — chat needs full-duplex; live dashboards and notification feeds are fine with SSE's simpler one-way model.

**Challenge [Hard]:** Build a real-time chat endpoint:
- `WebSocket /ws/{room_id}` — clients join rooms; broadcast messages to room members
- `ConnectionManager` class tracks active connections per room
- `GET /stream/events` — SSE endpoint that yields a timestamp event every second
- Gracefully handle disconnects (`WebSocketDisconnect`)

---

### Day 19 — File Uploads & Storage
**Concepts:** `UploadFile`, `File()`, chunked streaming, saving to disk vs cloud (S3 via `boto3`/`aioboto3`), `python-multipart`

**Concept anchor:** When a file arrives at your server, it doesn't have to be loaded entirely into memory before processing. Streaming reads it in fixed-size chunks — a buffer at a time — keeping memory usage constant regardless of file size. This is the same principle behind video streaming: you watch while it downloads. Buffering is a universal systems concept: it smooths out the mismatch between a fast producer and a slow consumer by staging data in an intermediate store.

**Challenge [Medium]:** Build a file upload service:
- `POST /upload` accepts multipart; validates MIME type (images only) and size (< 5MB)
- Streams file to disk without loading fully into memory
- Returns a UUID-based filename and a `GET /files/{uuid}` download endpoint
- `GET /files/{uuid}` uses `FileResponse`; returns 404 if not found
- Write tests using `httpx` with `files=` parameter

---

### Day 20 — Django Crash Course
**Concepts:** MTV pattern, ORM (`QuerySet`, `select_related`, `prefetch_related`), admin, `class-based views`, `django-rest-framework` basics

**Concept anchor:** Model-View-Controller (MVC) — Django calls it MTV — separates data, display logic, and request handling into distinct layers. This is separation of concerns applied at the framework level: each layer can change independently. An ORM (Object-Relational Mapper) abstracts the database behind Python objects, translating your code into SQL automatically — at the cost of occasionally hiding expensive queries, which is why `select_related` and `prefetch_related` exist to give you back explicit control.

**Challenge [Medium]:** Bootstrap a Django project with one app `blog`:
- Models: `Post`, `Comment` (FK to Post), `Tag` (M2M to Post)
- Register all in Django Admin with list filters
- DRF `ModelSerializer` + `ViewSet` for `Post` with nested comment count
- `GET /api/posts/?tag=python` filter
- One management command `python manage.py seed_data` that creates 10 dummy posts

---

### Day 21 — Week 3 Review Challenge
**Concept anchor:** Individual components (cache, queue, WebSocket, file storage) each work in isolation, but combining them introduces new failure modes — what happens if a cached task list is stale when a WebSocket pushes an update? What if a Celery worker fails mid-task? Integration tests exist specifically to catch behaviours that only appear when subsystems interact. This is emergent complexity: the system as a whole is harder to reason about than the sum of its parts.

**Challenge [Expert]:** Extend the Task Manager API from Day 14:
- Add Redis caching for task list queries
- Add a Celery task `send_due_reminder` that runs daily (use `celery beat`) and emails users with tasks due tomorrow (mock email with logging)
- Add a WebSocket endpoint `WS /ws/tasks` that broadcasts task updates to connected clients when any task changes status
- Add a file attachment endpoint `POST /tasks/{id}/attachments`
- Write integration tests covering the caching layer (assert cache hit/miss)

---

## Week 4 — Frontend Integration, Testing & Deployment

### Day 22 — Jinja2 Templates (Server-Side Rendering)
**Concepts:** `TemplateResponse`, template inheritance (`{% extends %}`), filters, context, static files, `url_for`

**Concept anchor:** In server-side rendering (SSR), the server assembles a complete HTML page and sends it to the browser — simple, fast to first paint, and works without JavaScript. In client-side rendering (React, Vue), the browser downloads JavaScript and builds the page itself from JSON data. SSR trades interactivity for simplicity; CSR trades simplicity for richer user experience. Template inheritance is the same composition idea from OOP: a base template defines the structure, child templates override specific blocks.

**Challenge [Easy]:** Build a FastAPI app serving HTML:
- `GET /` renders `index.html` showing a list of tasks from in-memory storage
- `GET /tasks/{id}` renders a detail page
- Base template with nav bar, child templates via `{% block content %}`
- A custom Jinja2 filter `{{ due_date | days_until }}` that shows "3 days left"

---

### Day 23 — HTMX: Interactivity Without JS Frameworks
**Concepts:** `hx-get`, `hx-post`, `hx-target`, `hx-swap`, `hx-trigger`, partial HTML responses, out-of-band swaps

**Concept anchor:** REST's original vision was that HTML itself carries the actions a user can take — links and forms are the interface, not a separate JSON API. This idea is called HATEOAS (Hypermedia as the Engine of Application State). HTMX returns to this model: instead of a JavaScript app calling a JSON API and rendering the result, the server returns HTML fragments directly and the browser swaps them into the page. This eliminates the need for a separate frontend codebase entirely.

**Challenge [Medium]:** Make the Day 22 app interactive with HTMX:
- Add task form with `hx-post="/tasks"` — server returns just the new `<li>` fragment
- Delete button with `hx-delete` and `hx-confirm` prompt; server returns empty 200
- Status toggle with `hx-patch`; server returns updated status badge fragment
- Search input with `hx-get="/tasks/search?q=..."` and `hx-trigger="keyup delay:300ms"` for live filtering
- No page reloads — all interactions are partial HTML swaps

---

### Day 24 — Streamlit & Dash (Data-Centric UIs)
**Concepts:** Streamlit widgets, `st.session_state`, caching (`@st.cache_data`), Plotly charts, Dash callbacks, `dcc.Graph`

**Concept anchor:** Reactive programming treats the UI as a pure function of state — when state changes, the display updates automatically without you manually wiring events to DOM updates. Streamlit's model is extreme: the entire Python script reruns on every user interaction. This is simple to reason about (just read the script top to bottom) but expensive, which is why `@st.cache_data` and `st.session_state` exist to persist values across reruns selectively.

**Challenge [Medium]:** Build a Streamlit dashboard that:
- Loads a CSV of sales data (you can generate it)
- Shows KPI metrics: total revenue, avg order value, top product
- A date range picker that filters data reactively
- A Plotly line chart of revenue over time
- A bar chart of top 10 products
- Cache the data load with `@st.cache_data(ttl=300)`

---

### Day 25 — Docker & Docker Compose
**Concepts:** `Dockerfile` best practices (multi-stage, layer caching), `.dockerignore`, `docker-compose.yml`, health checks, environment variables, named volumes

**Concept anchor:** A container is an isolated process with its own filesystem, network, and process tree — it cannot see the host OS or other containers unless explicitly permitted. This uses Linux kernel features (namespaces, cgroups) to create lightweight isolation without a full virtual machine. Immutable infrastructure means you never modify a running container; instead you rebuild the image and redeploy. This eliminates "works on my machine" problems by making the entire environment reproducible and version-controlled.

**Challenge [Hard]:** Containerize the Task Manager API (Day 14/21):
- Multi-stage `Dockerfile`: builder stage installs deps, final stage is slim
- `docker-compose.yml` with services: `api`, `postgres`, `redis`, `celery_worker`, `celery_beat`
- Health checks on `postgres` and `redis`; `api` depends on both being healthy
- Alembic migrations run as a one-shot `migrate` service before `api` starts
- Environment config via `.env` file (never hardcoded in compose)

---

### Day 26 — CI/CD with GitHub Actions
**Concepts:** Workflow YAML, jobs, steps, matrix builds, caching pip/uv, secrets, deploy on merge to main

**Concept anchor:** Continuous integration means every code change is automatically built and tested before merging — catching regressions when they're cheap to fix (on the branch) rather than expensive (in production). A deterministic build produces the same output given the same inputs every time: pinned dependency versions and layer caching are what make builds deterministic. A build that gives different results on different days is fundamentally untrustworthy, regardless of whether it passes.

**Challenge [Medium]:** Write a `.github/workflows/ci.yml` that:
- Triggers on push and PR to `main`
- Matrix: Python 3.11 and 3.12
- Steps: checkout → setup Python → cache deps → install → lint (`ruff`) → type check (`mypy`) → test (`pytest --cov`) → upload coverage to Codecov
- A second workflow `deploy.yml` that triggers on merge to `main` and SSHes into a server to `docker compose pull && docker compose up -d` (use `appleboy/ssh-action`)

---

### Day 27 — API Design Patterns
**Concepts:** REST vs GraphQL vs gRPC, pagination strategies (cursor vs offset), versioning (`/v1/`), idempotency keys, rate limiting (`slowapi`), OpenAPI customization

**Concept anchor:** Idempotency means an operation produces the same result whether called once or ten times — essential for safely retrying failed network requests without double-charging or double-creating. Rate limiting is a safety property, not just politeness: it prevents a single client from exhausting shared resources and degrading service for everyone else. Cursor-based pagination avoids the "missing row" problem of offset pagination when data is inserted mid-page, making it the correct choice for any frequently-updated dataset.

**Challenge [Hard]:** Harden the Task Manager API:
- Add cursor-based pagination to `GET /tasks` (return `next_cursor` in response)
- Add rate limiting: 100 req/min per user using `slowapi`
- Add an idempotency key header to `POST /tasks` — duplicate requests return the cached response
- Add API versioning prefix `/api/v1/`
- Customize OpenAPI: add tag descriptions, example values on all schemas, `operationId` on all routes

---

### Day 28 — Observability: Logging, Metrics & Tracing
**Concepts:** Structured logging (`structlog`), `prometheus-fastapi-instrumentator`, OpenTelemetry, Sentry, health check endpoints

**Concept anchor:** The three pillars of observability are logs, metrics, and traces. Logs are discrete events ("user 42 logged in at 14:03"). Metrics are numerical measurements aggregated over time ("500 requests/second, p99 latency 120ms"). Traces follow a single request through multiple services, showing where time was spent. Together they answer three different questions: what happened, how is the system performing overall, and where did this specific slow request go wrong.

**Challenge [Medium]:** Add observability to the API:
- Replace `print`/`logging` with `structlog` (JSON output in prod, pretty in dev)
- Add `GET /health` (liveness) and `GET /ready` (readiness — checks DB + Redis)
- Expose Prometheus metrics at `GET /metrics` using `prometheus-fastapi-instrumentator`
- Add Sentry SDK with a test `GET /debug/sentry` route that intentionally raises
- Log request ID (from header or generated UUID) on every log line using middleware

---

### Day 29 — Security Hardening
**Concepts:** SQL injection prevention, CORS, CSP headers, `python-multipart` size limits, secret rotation, `secrets` module, OWASP Top 10 in Python context

**Concept anchor:** Defense in depth means no single security control is relied upon alone — layers of controls ensure that bypassing one check does not mean total compromise. SQL injection and XSS remain in the OWASP Top 10 because they are still widely exploited despite being well understood: both involve an attacker supplying input that the application treats as code rather than data. Parameterised queries fix SQL injection by separating the query structure from its inputs at the protocol level — the database never interprets user input as SQL syntax.

**Challenge [Hard]:** Security audit and fix the Task Manager API:
1. Ensure all DB queries use parameterized statements (no f-string SQL anywhere)
2. Add `SecurityHeadersMiddleware` that sets `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, `Content-Security-Policy`
3. Implement account lockout: after 5 failed logins, lock account for 15 minutes (store in Redis)
4. Add `POST /auth/logout` that invalidates the JWT via a Redis blocklist
5. Write a security test suite: attempt SQL injection payloads, test locked account behavior, test blocklisted token rejection

---

### Day 30 — Final Capstone Challenge
**Concept anchor:** A production application is defined not just by its features but by its operational properties — how it handles load, how it fails gracefully, how it is monitored and deployed. The capstone forces you to make every architectural decision yourself: which data lives in Postgres vs Redis, how votes stay consistent under concurrency, how WebSocket clients stay in sync with REST state. This is where the difference between knowing individual tools and understanding how systems are composed becomes concrete.

**Challenge [Expert]:** Build **"QuickPoll"** — a real-time polling app, from scratch, production-ready:

**Features:**
- Auth: register, login, JWT
- `POST /polls` — create a poll with a question and 2–5 options (Pydantic validation)
- `POST /polls/{id}/vote` — one vote per user per poll (idempotent); update tally atomically in Redis (`HINCRBY`)
- `GET /polls/{id}` — returns question + options + live vote counts
- `WebSocket /ws/polls/{id}` — broadcasts updated tallies to all viewers in real time when a vote is cast
- `GET /polls/{id}/results` — Streamlit page rendering a live bar chart (polls the REST API every 2s via `st.rerun()`)
- Fully Dockerized (API + Redis + Streamlit)
- GitHub Actions CI pipeline
- Structured logging, `/health`, `/metrics`
- 80%+ test coverage

---

## Quick Reference: Key Libraries

| Area | Library |
|---|---|
| API Framework | FastAPI, Django + DRF |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.0, Django ORM |
| Migrations | Alembic, Django Migrations |
| Async DB driver | asyncpg, aiosqlite |
| Auth | python-jose / PyJWT, passlib |
| Caching | redis-py / aioredis |
| Task Queue | Celery + Redis |
| Testing | pytest, pytest-asyncio, httpx |
| Linting | ruff, mypy |
| Templates | Jinja2, HTMX |
| Data UI | Streamlit, Dash |
| Containers | Docker, Docker Compose |
| Logging | structlog |
| Metrics | prometheus-fastapi-instrumentator |

---

## Exam Focus Areas (High Weight)

1. Pydantic models and validation patterns
2. FastAPI dependency injection
3. SQLAlchemy 2.0 async patterns
4. JWT authentication flow
5. pytest fixtures and async testing
6. Docker Compose multi-service setup
7. REST API design (pagination, versioning, error responses)
8. Redis caching patterns
9. Background tasks vs Celery tasks (when to use which)
10. Security: parameterized queries, headers, rate limiting
