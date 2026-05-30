# Day 0 — Environment Setup & 30-Day Roadmap

---

## 1. Install Python

Download Python 3.12 from https://www.python.org/downloads/

**Windows install checklist:**
- Check "Add Python to PATH" during install — critical
- Check "Use admin privileges when installing py.exe"

Verify it worked:
```bash
python --version
# → Python 3.12.x
```

---

## 2. Install uv — The Modern Package Manager

`uv` replaces `pip` + `venv` with a single, much faster tool. The 30-day plan uses it throughout.

```bash
pip install uv
```

Verify:
```bash
uv --version
```

---

## 3. VS Code Setup

Install VS Code if you haven't. Then install these extensions:

| Extension | Purpose |
|---|---|
| **Python** (Microsoft) | Language support, debugger |
| **Pylance** (Microsoft) | Autocomplete, type checking |
| **Ruff** | Linting and formatting |

**VS Code settings to add** (`Ctrl+Shift+P` → "Open User Settings JSON"):
```json
{
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "python.analysis.typeCheckingMode": "basic"
}
```

This auto-formats your code on every save and highlights type errors.

---

## 4. Start a New Project — the Right Way

Every project gets its own isolated environment. Here's the workflow you'll use every day:

```bash
# Create and enter your project folder
mkdir my_project
cd my_project

# Initialize with uv (creates pyproject.toml + .venv automatically)
uv init

# Add a dependency
uv add requests

# Run a file
uv run main.py

# Or activate the venv and use Python directly
.venv\Scripts\activate        # Windows
python main.py
```

For each day's challenge folder, run `uv init` once at the start.

---

## 5. The REPL — Use It Daily

The Python REPL is your scratchpad. Open it by typing `python` in your terminal.

```python
>>> x = [1, 2, 3, 4, 5]
>>> x[1:3]
[2, 3]
>>> "hello".upper()
'HELLO'
>>> type(42)
<class 'int'>
>>> help(str.split)   # read docs for any built-in
```

When you're unsure how something works — try it in the REPL first. It's faster than writing a file and running it.

Exit with `exit()` or `Ctrl+Z` then Enter (Windows).

---

## 6. Running Python Files

```bash
python filename.py         # run a file
python -m module_name      # run a module as a script (e.g. python -m pytest)
python -c "print('hello')" # run a one-liner
```

---

## 7. Reading Error Messages

Python errors are called **tracebacks**. Read them bottom to top:

```
Traceback (most recent call last):
  File "main.py", line 10, in <module>
    result = divide(10, 0)
  File "main.py", line 5, in divide
    return a / b
ZeroDivisionError: division by zero
```

- **Bottom line**: the actual error type and message — start here
- **Lines above**: the path the code took to get there — read upward to understand context

---

## 8. The 30-Day Roadmap at a Glance

```
Week 1 — Modern Python Foundations
  Day 1  Type hints + Pydantic          ← data validation
  Day 2  Async Python                   ← concurrent code
  Day 3  Decorators + context managers  ← code patterns
  Day 4  Iterators + generators         ← memory-efficient data
  Day 5  Testing with pytest            ← proving your code works
  Day 6  Packaging + project structure  ← professional layout
  Day 7  Review challenge (CLI tool)

Week 2 — FastAPI Backend
  Day 8   FastAPI basics                ← building APIs
  Day 9   Dependency injection + middleware
  Day 10  Async routes + background tasks
  Day 11  SQLAlchemy + Alembic          ← databases
  Day 12  FastAPI + database integration
  Day 13  JWT authentication            ← login/auth systems
  Day 14  Review challenge (Task Manager API)

Week 3 — Databases, Caching & Advanced Backend
  Day 15  PostgreSQL deep dive
  Day 16  Redis caching + pub/sub
  Day 17  Celery task queues            ← background jobs
  Day 18  WebSockets + SSE              ← real-time features
  Day 19  File uploads + storage
  Day 20  Django crash course
  Day 21  Review challenge

Week 4 — Frontend Integration, Testing & Deployment
  Day 22  Jinja2 templates              ← server-rendered HTML
  Day 23  HTMX                          ← interactivity without JS frameworks
  Day 24  Streamlit + Dash              ← data dashboards
  Day 25  Docker + Docker Compose       ← containers
  Day 26  CI/CD with GitHub Actions
  Day 27  API design patterns
  Day 28  Observability (logging, metrics)
  Day 29  Security hardening
  Day 30  Final capstone: QuickPoll
```

---

## 9. How Each Day Works

Each day folder contains:
- `concepts.md` — explanation of the day's topics with code examples
- `challenge.md` — the coding challenge with requirements

**Suggested daily routine (~2-3 hours):**
1. Read `concepts.md` fully before writing any code (30 min)
2. Open the REPL and experiment with the examples as you read
3. Set up the day's project folder with `uv init`
4. Attempt the challenge from scratch (don't look at solutions — struggle is how you learn)
5. If stuck for more than 20 minutes on one thing, ask for a hint rather than giving up

---

## 10. Tools Reference Card

| Tool | Command | Purpose |
|---|---|---|
| Python REPL | `python` | Interactive testing |
| Run a file | `python file.py` | Execute script |
| Install package | `uv add <package>` | Add dependency |
| Run tests | `python -m pytest` | Run your test suite |
| Type check | `python -m mypy file.py` | Static type check |
| Format code | `ruff format .` | Auto-format all files |
| Lint code | `ruff check .` | Find code issues |
| See installed packages | `uv pip list` | List dependencies |

---

## 11. Mindset for 30 Days

**Confusion is normal and means you're learning.** Python looks easy at first (readable syntax, no semicolons) but depth appears quickly as soon as you hit async code, decorators, or class hierarchies. That confusion is the work.

**Type the code, don't copy-paste.** Your muscle memory and understanding both improve when you type it yourself, even when copying from examples.

**The error message is your friend.** Every `TypeError` or `AttributeError` is Python telling you exactly what went wrong. Read it before asking for help.

**Week 1 is the most important.** Days 1–7 build the foundation that every later day assumes. If something from Week 1 is unclear, revisit it before moving forward.
