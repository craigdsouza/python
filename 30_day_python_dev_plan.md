# 30-Day Python Developer Exam Prep Plan

Modern Python stack: backend (FastAPI, Django, SQLAlchemy, async), frontend integration (Jinja2, HTMX, Streamlit), databases, testing, and deployment.

---

## How to Use This Plan

- Each day has a **concept block** (read/watch) and a **coding challenge**.
- Challenges are rated: `[Easy]` `[Medium]` `[Hard]` `[Expert]`
- Difficulty ramps gradually — Week 1 is foundations, Week 4 is production-grade.
- Time budget: ~2–3 hours/day.

---

## Week 1 — Modern Python Foundations

### Day 1 — Type Hints & Pydantic
**Concepts:** `typing` module, `Annotated`, `TypeVar`, Pydantic v2 models, validators, `model_dump()`

**Challenge [Easy]:** Define a Pydantic `User` model with fields: `id: int`, `email: EmailStr`, `age: int` (must be 18–99), `role: Literal["admin", "user"]`. Write a function that accepts a raw dict, validates it, and returns the model or raises a `ValidationError`. Test with both valid and invalid inputs.

---

### Day 2 — Async Python
**Concepts:** `async`/`await`, `asyncio.gather`, `asyncio.create_task`, event loop, `asyncio.Queue`, avoiding blocking calls

**Challenge [Easy]:** Write an async function `fetch_all(urls: list[str])` that uses `asyncio.gather` with `asyncio.sleep` as a mock for HTTP delay (random 0.1–0.5s per URL). Print results in completion order and total elapsed time. Show why sequential would be slower.

---

### Day 3 — Decorators & Context Managers
**Concepts:** `functools.wraps`, parametrized decorators, `__enter__`/`__exit__`, `contextlib.contextmanager`, class-based context managers

**Challenge [Medium]:** Build a `@retry(times=3, delay=0.5, exceptions=(ValueError,))` decorator that retries a function on specified exceptions. Also build a `timer()` context manager that logs elapsed time. Compose both on a flaky mock function.

---

### Day 4 — Iterators, Generators & dataclasses
**Concepts:** `__iter__`/`__next__`, generator expressions, `yield from`, `@dataclass`, `field()`, `__post_init__`, `slots=True`

**Challenge [Medium]:** Implement a `Paginator` dataclass that wraps a list and yields pages of `n` items as a generator. Add a `total_pages` property and make it iterable with `__iter__`. Then write a pipeline using generator chaining to: read lines → filter blanks → parse as CSV row → yield dicts.

---

### Day 5 — Testing with pytest
**Concepts:** `pytest` fixtures, `conftest.py`, parametrize, `pytest-mock`, `monkeypatch`, coverage, `pytest-asyncio`

**Challenge [Medium]:** Write a `Calculator` class with `add`, `divide` (raises `ZeroDivisionError`), and a `history` list. Write a full pytest suite: parametrized tests, a fixture that resets history, a mock for an external `log_operation(op)` call, and one async test using `pytest-asyncio`.

---

### Day 6 — Python Packaging & Project Structure
**Concepts:** `pyproject.toml`, `uv` / `pip-tools`, virtual environments, `__init__.py`, relative imports, `src/` layout

**Challenge [Easy]:** Scaffold a project with `src/myapp/` layout containing two modules. Add `pyproject.toml` with metadata and dependencies. Write a `cli.py` entry point using `argparse` that accepts `--name` and `--count` and prints a greeting N times. Install it in editable mode and run via `myapp`.

---

### Day 7 — Week 1 Review Challenge
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

**Challenge [Easy]:** Build a FastAPI app with:
- `GET /items/{item_id}` — returns item or 404
- `POST /items` — accepts a Pydantic body, stores in-memory dict
- `GET /items?skip=0&limit=10` — paginated list
- Response model that excludes internal fields

---

### Day 9 — Dependency Injection & Middleware
**Concepts:** `Depends()`, dependency chaining, `yield` dependencies, `BaseHTTPMiddleware`, CORS, request timing middleware

**Challenge [Medium]:** Add to yesterday's app:
- A `get_current_user` dependency that reads a fake `X-Token` header (hardcoded valid tokens)
- Protect `POST /items` with it
- Add a request-timing middleware that logs method, path, and elapsed ms
- Add CORS middleware allowing `http://localhost:3000`

---

### Day 10 — Async FastAPI + Background Tasks
**Concepts:** `async def` routes, `BackgroundTasks`, `asyncio.sleep` vs `time.sleep` in async context, `lifespan` events

**Challenge [Medium]:** Build a `POST /reports/generate` endpoint that:
- Immediately returns `{ "job_id": "uuid", "status": "queued" }`
- Runs report generation as a `BackgroundTask` (mock: sleep 2s, write result to a dict)
- Exposes `GET /reports/{job_id}` to poll status (`queued` → `done` → result)
- Uses `lifespan` to initialize and tear down a shared in-memory "database" dict

---

### Day 11 — SQLAlchemy 2.0 + Alembic
**Concepts:** Declarative models, `Session`, `select()`, relationships (`relationship()`), `joinedload`, Alembic migrations, `AsyncSession`

**Challenge [Medium]:** Define SQLAlchemy models `Author` and `Book` (one-to-many). Use Alembic to generate and apply a migration. Write CRUD functions: create author, add book, get all books by author (with joined load). Use SQLite for simplicity.

---

### Day 12 — FastAPI + Database Integration
**Concepts:** `get_db` dependency with `yield`, request-scoped sessions, async SQLAlchemy, connection pooling

**Challenge [Hard]:** Wire Day 11's models into a FastAPI app:
- `POST /authors` + `GET /authors/{id}/books`
- `POST /authors/{id}/books`
- `DELETE /books/{id}` (cascade check)
- Use `AsyncSession` with `asyncpg` (or SQLite async driver)
- Dependency that provides a session per request and rolls back on exception

---

### Day 13 — Authentication: JWT + OAuth2
**Concepts:** `OAuth2PasswordBearer`, `python-jose` / `PyJWT`, hashing with `passlib`, token expiry, refresh tokens

**Challenge [Hard]:** Add auth to the books API:
- `POST /auth/register` — hash password with bcrypt, store user
- `POST /auth/login` — verify password, return `access_token` (JWT, 30min) + `refresh_token` (24h)
- `POST /auth/refresh` — exchange refresh token for new access token
- Protect all write endpoints; `GET` endpoints are public
- Return `401` on expired/invalid tokens

---

### Day 14 — Week 2 Review Challenge
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

**Challenge [Medium]:** Write raw SQL (via `asyncpg` or `psycopg3`) for:
1. A query using `tsvector` full-text search on a `posts` table
2. A transaction that transfers "credits" between two users with `SELECT FOR UPDATE` (no negative balances)
3. Add a `GIN` index and show the `EXPLAIN` output before/after

---

### Day 16 — Redis: Caching & Pub/Sub
**Concepts:** `redis-py` / `aioredis`, cache-aside pattern, TTL, `SETEX`, pub/sub, Redis as a job queue

**Challenge [Medium]:** Add to the books API:
- Cache `GET /authors/{id}/books` in Redis with 60s TTL; invalidate on write
- A `POST /notifications/publish` that publishes to a Redis channel
- A background subscriber that logs received messages
- Write a helper `@cached(ttl=60, key_fn=...)` decorator

---

### Day 17 — Celery & Task Queues
**Concepts:** Celery workers, brokers (Redis/RabbitMQ), `@shared_task`, `apply_async`, `chain`/`chord`/`group`, retries, task state

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

**Challenge [Hard]:** Build a real-time chat endpoint:
- `WebSocket /ws/{room_id}` — clients join rooms; broadcast messages to room members
- `ConnectionManager` class tracks active connections per room
- `GET /stream/events` — SSE endpoint that yields a timestamp event every second
- Gracefully handle disconnects (`WebSocketDisconnect`)

---

### Day 19 — File Uploads & Storage
**Concepts:** `UploadFile`, `File()`, chunked streaming, saving to disk vs cloud (S3 via `boto3`/`aioboto3`), `python-multipart`

**Challenge [Medium]:** Build a file upload service:
- `POST /upload` accepts multipart; validates MIME type (images only) and size (< 5MB)
- Streams file to disk without loading fully into memory
- Returns a UUID-based filename and a `GET /files/{uuid}` download endpoint
- `GET /files/{uuid}` uses `FileResponse`; returns 404 if not found
- Write tests using `httpx` with `files=` parameter

---

### Day 20 — Django Crash Course
**Concepts:** MTV pattern, ORM (`QuerySet`, `select_related`, `prefetch_related`), admin, `class-based views`, `django-rest-framework` basics

**Challenge [Medium]:** Bootstrap a Django project with one app `blog`:
- Models: `Post`, `Comment` (FK to Post), `Tag` (M2M to Post)
- Register all in Django Admin with list filters
- DRF `ModelSerializer` + `ViewSet` for `Post` with nested comment count
- `GET /api/posts/?tag=python` filter
- One management command `python manage.py seed_data` that creates 10 dummy posts

---

### Day 21 — Week 3 Review Challenge
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

**Challenge [Easy]:** Build a FastAPI app serving HTML:
- `GET /` renders `index.html` showing a list of tasks from in-memory storage
- `GET /tasks/{id}` renders a detail page
- Base template with nav bar, child templates via `{% block content %}`
- A custom Jinja2 filter `{{ due_date | days_until }}` that shows "3 days left"

---

### Day 23 — HTMX: Interactivity Without JS Frameworks
**Concepts:** `hx-get`, `hx-post`, `hx-target`, `hx-swap`, `hx-trigger`, partial HTML responses, out-of-band swaps

**Challenge [Medium]:** Make the Day 22 app interactive with HTMX:
- Add task form with `hx-post="/tasks"` — server returns just the new `<li>` fragment
- Delete button with `hx-delete` and `hx-confirm` prompt; server returns empty 200
- Status toggle with `hx-patch`; server returns updated status badge fragment
- Search input with `hx-get="/tasks/search?q=..."` and `hx-trigger="keyup delay:300ms"` for live filtering
- No page reloads — all interactions are partial HTML swaps

---

### Day 24 — Streamlit & Dash (Data-Centric UIs)
**Concepts:** Streamlit widgets, `st.session_state`, caching (`@st.cache_data`), Plotly charts, Dash callbacks, `dcc.Graph`

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

**Challenge [Hard]:** Containerize the Task Manager API (Day 14/21):
- Multi-stage `Dockerfile`: builder stage installs deps, final stage is slim
- `docker-compose.yml` with services: `api`, `postgres`, `redis`, `celery_worker`, `celery_beat`
- Health checks on `postgres` and `redis`; `api` depends on both being healthy
- Alembic migrations run as a one-shot `migrate` service before `api` starts
- Environment config via `.env` file (never hardcoded in compose)

---

### Day 26 — CI/CD with GitHub Actions
**Concepts:** Workflow YAML, jobs, steps, matrix builds, caching pip/uv, secrets, deploy on merge to main

**Challenge [Medium]:** Write a `.github/workflows/ci.yml` that:
- Triggers on push and PR to `main`
- Matrix: Python 3.11 and 3.12
- Steps: checkout → setup Python → cache deps → install → lint (`ruff`) → type check (`mypy`) → test (`pytest --cov`) → upload coverage to Codecov
- A second workflow `deploy.yml` that triggers on merge to `main` and SSHes into a server to `docker compose pull && docker compose up -d` (use `appleboy/ssh-action`)

---

### Day 27 — API Design Patterns
**Concepts:** REST vs GraphQL vs gRPC, pagination strategies (cursor vs offset), versioning (`/v1/`), idempotency keys, rate limiting (`slowapi`), OpenAPI customization

**Challenge [Hard]:** Harden the Task Manager API:
- Add cursor-based pagination to `GET /tasks` (return `next_cursor` in response)
- Add rate limiting: 100 req/min per user using `slowapi`
- Add an idempotency key header to `POST /tasks` — duplicate requests return the cached response
- Add API versioning prefix `/api/v1/`
- Customize OpenAPI: add tag descriptions, example values on all schemas, `operationId` on all routes

---

### Day 28 — Observability: Logging, Metrics & Tracing
**Concepts:** Structured logging (`structlog`), `prometheus-fastapi-instrumentator`, OpenTelemetry, Sentry, health check endpoints

**Challenge [Medium]:** Add observability to the API:
- Replace `print`/`logging` with `structlog` (JSON output in prod, pretty in dev)
- Add `GET /health` (liveness) and `GET /ready` (readiness — checks DB + Redis)
- Expose Prometheus metrics at `GET /metrics` using `prometheus-fastapi-instrumentator`
- Add Sentry SDK with a test `GET /debug/sentry` route that intentionally raises
- Log request ID (from header or generated UUID) on every log line using middleware

---

### Day 29 — Security Hardening
**Concepts:** SQL injection prevention, CORS, CSP headers, `python-multipart` size limits, secret rotation, `secrets` module, OWASP Top 10 in Python context

**Challenge [Hard]:** Security audit and fix the Task Manager API:
1. Ensure all DB queries use parameterized statements (no f-string SQL anywhere)
2. Add `SecurityHeadersMiddleware` that sets `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, `Content-Security-Policy`
3. Implement account lockout: after 5 failed logins, lock account for 15 minutes (store in Redis)
4. Add `POST /auth/logout` that invalidates the JWT via a Redis blocklist
5. Write a security test suite: attempt SQL injection payloads, test locked account behavior, test blocklisted token rejection

---

### Day 30 — Final Capstone Challenge
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
