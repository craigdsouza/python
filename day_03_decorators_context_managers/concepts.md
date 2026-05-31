# Day 3 — Decorators & Context Managers

---

## Concept Anchor

A **decorator** is a higher-order function — it takes a function as input and returns a new function. This works because Python treats functions as first-class values: you can pass them around, store them in variables, and return them from other functions, just like integers or strings. This is a foundational idea in functional programming.

**Context managers** implement RAII (Resource Acquisition Is Initialization): resources like file handles and database connections are guaranteed to be released when a block exits — even if an exception occurs. The resource is acquired on entry and released on exit, and the language enforces this automatically.

---

## 1. Functions as Values — The Foundation

Before decorators make sense, you need to see that functions are just values:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

# Assign to a variable
say_hello = greet
print(say_hello("Alice"))   # "Hello, Alice"

# Pass as an argument
def call_twice(fn, value):
    print(fn(value))
    print(fn(value))

call_twice(greet, "Bob")

# Return from a function
def make_greeter(prefix: str):
    def inner(name: str) -> str:
        return f"{prefix}, {name}"
    return inner   # returns the function itself, not its result

hi = make_greeter("Hi")
print(hi("Carol"))   # "Hi, Carol"
```

`inner` is defined inside `make_greeter` and **closes over** the `prefix` variable — this is called a **closure**.

---

## 2. Basic Decorators

A decorator wraps a function with extra behavior before and/or after the original call.

```python
def shout(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        return result.upper()
    return wrapper

@shout
def greet(name: str) -> str:
    return f"hello, {name}"

print(greet("alice"))   # "HELLO, ALICE"
```

`@shout` is syntactic sugar for `greet = shout(greet)`. Nothing magic — it's just reassigning the name.

The `*args, **kwargs` pattern lets the wrapper accept any arguments and pass them through unchanged, so the decorator works on any function signature.

---

## 3. `functools.wraps` — Preserving Metadata

Without `functools.wraps`, the wrapped function loses its original name and docstring:

```python
def shout(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).upper()
    return wrapper

@shout
def greet(name: str) -> str:
    """Greets a person."""
    return f"hello, {name}"

print(greet.__name__)   # "wrapper"  ← wrong!
print(greet.__doc__)    # None       ← wrong!
```

`functools.wraps` fixes this by copying the original function's metadata onto the wrapper:

```python
import functools

def shout(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).upper()
    return wrapper

@shout
def greet(name: str) -> str:
    """Greets a person."""
    return f"hello, {name}"

print(greet.__name__)   # "greet"           ← correct
print(greet.__doc__)    # "Greets a person." ← correct
```

Always use `@functools.wraps(fn)` inside decorator wrappers — it matters for debugging, documentation, and tools like `pytest`.

---

## 4. Parametrized Decorators

Sometimes you want to pass arguments to a decorator: `@retry(times=3)`. This requires one extra layer of nesting — a function that receives the arguments and returns the actual decorator.

```python
import functools
import time

def retry(times: int = 3, delay: float = 0.5):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < times:
                        time.sleep(delay)
            raise RuntimeError(f"All {times} attempts failed")
        return wrapper
    return decorator

@retry(times=3, delay=0.2)
def unstable():
    import random
    if random.random() < 0.7:
        raise ValueError("flaky!")
    return "success"
```

The call chain is: `retry(times=3, delay=0.2)` → returns `decorator` → `decorator(unstable)` → returns `wrapper`.

---

## 5. Context Managers — `__enter__` and `__exit__`

A context manager is any object that implements two methods:

- `__enter__` — runs when entering the `with` block, returns the resource
- `__exit__` — runs when leaving the block, even if an exception occurs

```python
class ManagedFile:
    def __init__(self, path: str, mode: str = "r"):
        self.path = path
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.path, self.mode)
        return self.file   # this becomes `f` in `with ManagedFile(...) as f:`

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        # Return False (or None) to let exceptions propagate
        # Return True to suppress exceptions — almost never what you want
        return False

with ManagedFile("data.txt") as f:
    content = f.read()
# file is closed here regardless of whether read() raised
```

`__exit__` receives three arguments describing any exception that occurred (`None, None, None` if no exception). Returning `False` lets the exception propagate; returning `True` would swallow it.

---

## 6. `contextlib.contextmanager` — Generator-Based Context Managers

Writing a class just to get `__enter__`/`__exit__` is verbose. `contextlib.contextmanager` lets you write a context manager as a generator function with a single `yield`:

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label: str = ""):
    start = time.perf_counter()
    try:
        yield   # execution passes to the `with` block here
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label} took {elapsed:.3f}s")

with timer("database query"):
    time.sleep(0.5)   # simulated work
# prints: "database query took 0.500s"
```

The code before `yield` is the `__enter__` phase. The code after (in `finally`) is the `__exit__` phase. Using `try/finally` ensures cleanup runs even if the `with` block raises an exception.

You can also yield a value:

```python
@contextmanager
def open_managed(path: str):
    f = open(path)
    try:
        yield f   # becomes `f` in `with open_managed(path) as f:`
    finally:
        f.close()
```

---

## 7. Class-Based vs Generator-Based Context Managers

| Approach | When to use |
|---|---|
| `@contextmanager` | Simple cases — setup, yield, teardown in one readable block |
| Class with `__enter__`/`__exit__` | When you need to store state, support reuse, or inherit |

Both produce identical behavior from the caller's perspective. Choose whichever is clearer for the complexity of your resource management.

---

## 8. Composing Decorators

Multiple decorators stack from bottom to top — the decorator closest to the function applies first:

```python
@log_calls        # applies second (outermost wrapper)
@retry(times=3)   # applies first (innermost wrapper)
def flaky_fn():
    ...

# Equivalent to:
flaky_fn = log_calls(retry(times=3)(flaky_fn))
```

When you call `flaky_fn()`, `log_calls`'s wrapper runs first, which calls the `retry` wrapper, which calls the original function.

---

## 9. Practical Patterns

### Timing decorator
```python
import functools
import time

def timed(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper
```

### Logging decorator
```python
import functools

def log_calls(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}({args}, {kwargs})")
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} returned {result!r}")
        return result
    return wrapper
```

### Suppressing specific exceptions (context manager)
```python
from contextlib import suppress

with suppress(FileNotFoundError):
    open("nonexistent.txt")
# no exception raised — contextlib.suppress is a built-in context manager
```

---

## Summary

| Concept | One-liner |
|---|---|
| Higher-order function | A function that takes or returns other functions |
| Closure | Inner function that captures variables from its enclosing scope |
| `@decorator` | Syntactic sugar for `fn = decorator(fn)` |
| `functools.wraps` | Copies `__name__`, `__doc__` etc. from the wrapped function onto the wrapper |
| Parametrized decorator | Extra outer function layer that accepts arguments and returns the decorator |
| `__enter__` / `__exit__` | Protocol methods that make an object usable as a `with` block |
| `@contextmanager` | Turn a generator function (with one `yield`) into a context manager |
| RAII | Guarantee resource cleanup on scope exit, even when exceptions occur |
