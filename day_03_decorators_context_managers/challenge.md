# Day 3 — Challenge: Retry Decorator & Timer Context Manager

**Difficulty:** Medium  
**Estimated time:** 60–90 minutes

---

## Goal

Build a parametrized `@retry` decorator and a `timer()` context manager, then compose them on a flaky mock function to see both tools working together.

---

## Requirements

### 1. A `@retry(times=3, delay=0.5, exceptions=(Exception,))` decorator

- `times` — how many total attempts to make (default 3)
- `delay` — seconds to wait between attempts (default 0.5)
- `exceptions` — a tuple of exception types that should trigger a retry (default `(Exception,)`)

Behavior:
- On each failed attempt, print `"Attempt {n}/{times} failed: {error}"`
- Wait `delay` seconds before the next attempt
- If all attempts are exhausted, re-raise the last exception
- If the exception is **not** in `exceptions`, do not retry — let it propagate immediately
- Use `functools.wraps` so the wrapped function keeps its original name and docstring

### 2. A `timer(label: str = "")` context manager

- Implemented using `@contextmanager` from `contextlib`
- Records elapsed time using `time.perf_counter()`
- On exit, prints: `"{label} completed in {elapsed:.3f}s"` (or just `"completed in {elapsed:.3f}s"` if no label)
- Must still print the time even if the `with` block raises an exception

### 3. A `flaky_mock(fail_times: int = 2) -> str` function

- Maintains a call counter (use a mutable default or a closure — your choice)
- Raises `ValueError("simulated failure")` for the first `fail_times` calls
- Returns `"success"` on the call after that
- Decorate it with `@retry(times=3, delay=0.1, exceptions=(ValueError,))`

### 4. Compose and run

In `if __name__ == "__main__"`:

1. Run `flaky_mock()` inside a `with timer("flaky_mock"):` block and print the result
2. Demonstrate that `retry` does **not** catch exceptions outside its `exceptions` tuple — call a function decorated with `@retry(times=3, exceptions=(ValueError,))` that raises `TypeError`, and show it propagates immediately (catch it in main and print a message)
3. Demonstrate exhausting all retries — call a function that always raises `ValueError`, wrap it in a `try/except`, and print `"All retries exhausted: {error}"`

---

## Expected output (example)

```
=== Test 1: flaky_mock with retry + timer ===
Attempt 1/3 failed: simulated failure
Attempt 2/3 failed: simulated failure
Result: success
flaky_mock completed in 0.201s

=== Test 2: wrong exception type — no retry ===
TypeError propagated immediately: wrong type

=== Test 3: all retries exhausted ===
Attempt 1/3 failed: always fails
Attempt 2/3 failed: always fails
Attempt 3/3 failed: always fails
All retries exhausted: always fails
```

(Exact times will vary.)

---

## Constraints

- Use only the standard library (`functools`, `time`, `contextlib`)
- `retry` must be a parametrized decorator (three levels of nesting: outer args → decorator → wrapper)
- `timer` must use `@contextmanager`, not a class
- Do not use `time.sleep` in the `timer` — only in `retry`

---

## Stretch Goals (optional)

1. Add an `exponential_backoff: bool = False` parameter to `@retry` — when `True`, multiply `delay` by `2` on each attempt (`0.1s`, `0.2s`, `0.4s`, ...)
2. Write a class-based `Timer` context manager that stores the elapsed time as `self.elapsed` so the caller can read it after the `with` block: `with Timer() as t: ...; print(t.elapsed)`
3. Write a `@memoize` decorator that caches the return value of a function based on its arguments — calling it again with the same args returns the cached result without re-executing. (Hint: use a `dict` as the cache, keyed on `(args, tuple(sorted(kwargs.items())))`)

---

## File to edit

`day_03_decorators_context_managers/solution.py`
