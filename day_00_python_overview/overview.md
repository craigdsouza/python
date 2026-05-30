# Day 0 — Python: The Big Picture

---

## 1. What Python Is (and Why It Exists)

Python was created in 1991 by Guido van Rossum. His goal was simple: make a language that reads almost like plain English, so programmers spend more time solving problems and less time fighting the language itself.

Python's guiding philosophy is captured in a document called **The Zen of Python**. Run `import this` in any Python terminal to see it. The core ideas:

- **Readability counts.** Code is read far more than it is written.
- **Explicit is better than implicit.** Don't hide what's happening.
- **There should be one obvious way to do it.** Less choice, less confusion.
- **Simple is better than complex.** Don't over-engineer.

This philosophy shapes every design decision in the language.

---

## 2. What Python Is Used For

Python is unusually versatile. The same language powers:

| Domain | Examples |
|---|---|
| **Backend APIs** | FastAPI, Django — what this 30-day plan focuses on |
| **Data science / ML** | NumPy, pandas, scikit-learn, PyTorch |
| **Scripting / automation** | Replacing bash scripts, file processing, web scraping |
| **Finance / quant** | Data pipelines, risk models |
| **DevOps tooling** | Ansible, AWS CDK, build tools |

You'll be learning Python through the backend lens, but the foundations carry over everywhere.

---

## 3. How Python Runs Your Code

Understanding this saves a lot of confusion later.

### Interpreted, not compiled

In C++, you compile your code into a binary executable before running it. Python doesn't do that — the Python interpreter reads your source file directly and executes it line by line.

```
your_code.py  →  Python interpreter  →  result
```

This means:
- Errors only appear when Python reaches the bad line (not before you run it)
- You can test snippets instantly in the **REPL** (more on this below)
- Python is slower than C++ for raw computation (but fast enough for nearly all backend work)

### The REPL — your best learning tool

REPL stands for Read-Eval-Print Loop. Type `python` (or `python3`) in your terminal and you get an interactive session:

```python
>>> 2 + 2
4
>>> name = "Craig"
>>> f"Hello, {name}"
'Hello, Craig'
>>> [x * 2 for x in range(5)]
[0, 2, 4, 6, 8]
```

Use this constantly. Whenever you're unsure how something works, test it here immediately. It's far faster than writing a file, running it, and checking.

---

## 4. Python's Type System — Dynamic Typing

Both Python and JavaScript are **dynamically typed** — you don't declare what type a variable holds, and the type can change.

```python
x = 10        # x is an int
x = "hello"   # now x is a string — perfectly valid
x = [1, 2, 3] # now x is a list
```

Compare to a statically typed language like Java or TypeScript where you'd write `int x = 10;` and it can only ever be an int.

**What this means in practice:**
- Writing code is faster — less ceremony
- Bugs can hide until runtime — a function might receive the wrong type and you won't know until it crashes
- Python added optional **type hints** (Day 1) to get the benefits of static typing without forcing it everywhere

The type of a value is always knowable — you can ask:

```python
type(42)        # <class 'int'>
type("hello")   # <class 'str'>
type([1, 2, 3]) # <class 'list'>
```

---

## 5. Core Data Types — What They're Called in Python

If you've written JavaScript, the concepts are the same but the names differ:

| Concept | JavaScript | Python |
|---|---|---|
| Whole number | `number` (42) | `int` (42) |
| Decimal number | `number` (3.14) | `float` (3.14) |
| Text | `string` ("hello") | `str` ("hello") |
| True/false | `boolean` | `bool` |
| Ordered list | `Array` ([1,2,3]) | `list` ([1,2,3]) |
| Key-value pairs | `Object` ({a:1}) | `dict` ({"a":1}) |
| Fixed ordered set | no direct equivalent | `tuple` ((1,2,3)) — immutable list |
| Unique collection | `Set` | `set` ({1,2,3}) |
| Nothing | `null` / `undefined` | `None` |

**Python has no `undefined`.** `None` is the one and only "absence of value."

---

## 6. Syntax — What's Different from What You Know

### Indentation is the structure

Python uses **indentation** (spaces/tabs) to define code blocks. There are no curly braces `{}`.

```python
# Python
def greet(name):
    if name == "Craig":
        print("Hey Craig!")
    else:
        print(f"Hello, {name}")
```

The 4-space indent *is* the structure. Getting this wrong causes an `IndentationError`. Use 4 spaces consistently — don't mix tabs and spaces.

### No semicolons

One statement per line. No `;` needed.

### `and`, `or`, `not` — not `&&`, `||`, `!`

```python
# Python
if age > 18 and is_verified:
    ...

if not is_logged_in:
    ...
```

### `True` / `False` — capital first letter

```python
is_active = True   # not 'true'
is_done = False    # not 'false'
```

### String formatting — f-strings

Python's preferred way to embed variables in strings:

```python
name = "Craig"
age = 30
print(f"My name is {name} and I am {age} years old.")
# → My name is Craig and I am 30 years old.
```

This is equivalent to JavaScript's template literals: `` `My name is ${name}` ``

### `elif` — not `else if`

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
```

---

## 7. Functions

Functions work the same conceptually as in JavaScript. Key differences:

```python
# Python function
def add(a, b):
    return a + b

result = add(3, 4)   # → 7
```

### Default arguments

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Craig")            # → "Hello, Craig!"
greet("Craig", "Hey")     # → "Hey, Craig!"
```

### Keyword arguments — call functions by name

This is something Python leans on heavily. You'll see it everywhere:

```python
def create_user(name, age, role="user"):
    ...

create_user(name="Craig", age=30, role="admin")  # order doesn't matter
```

### Functions are objects — you can pass them around

```python
def double(x):
    return x * 2

def apply(func, value):
    return func(value)

apply(double, 5)   # → 10
```

---

## 8. Everything is an Object

In Python, **everything** — numbers, strings, functions, even classes — is an object. Objects have **methods** (functions attached to them) and **attributes** (data attached to them).

You access them with dot notation:

```python
name = "craig dsouza"
name.upper()           # → "CRAIG DSOUZA"
name.split(" ")        # → ["craig", "dsouza"]
name.replace("craig", "Craig")  # → "Craig dsouza"

numbers = [3, 1, 4, 1, 5]
numbers.append(9)      # modifies the list in place
numbers.sort()         # sorts in place
len(numbers)           # → 6  (built-in function, not a method)
```

To see every method available on something: `dir(name)` or check the docs.

---

## 9. Classes — Blueprints for Objects

A class is a template for creating objects. Python is object-oriented at its core, and you'll see classes everywhere in the 30-day plan (Pydantic models, SQLAlchemy models, FastAPI routers are all class-based).

```python
class Dog:
    def __init__(self, name, breed):   # constructor — runs when you create a Dog
        self.name = name               # self = this specific instance
        self.breed = breed

    def bark(self):
        return f"{self.name} says: woof!"

my_dog = Dog("Rex", "Labrador")
my_dog.bark()    # → "Rex says: woof!"
my_dog.name      # → "Rex"
```

`self` is Python's equivalent of JavaScript's `this`. Unlike JS, you must explicitly write `self` as the first argument of every method.

### `__init__` and dunder methods

Methods with double underscores on both sides (called "dunder" or "magic" methods) have special meaning Python calls automatically:

| Dunder | When called |
|---|---|
| `__init__` | When the object is created |
| `__str__` | When you `print(obj)` |
| `__len__` | When you call `len(obj)` |
| `__repr__` | When you inspect the object in the REPL |

You don't need to memorize all of them now — just know they exist.

---

## 10. Modules and Imports

Python code is organized into **modules** (files) and **packages** (folders of files). To use code from another file or a library, you import it.

```python
import math
math.sqrt(16)         # → 4.0

from math import sqrt
sqrt(16)              # → 4.0

from math import sqrt, pi
pi                    # → 3.141592653589793
```

Standard library modules you'll use constantly:
- `os` — file system, environment variables
- `sys` — Python runtime info
- `datetime` — dates and times
- `json` — parse/write JSON
- `re` — regular expressions
- `pathlib` — file paths (better than `os.path`)
- `collections` — specialized containers
- `itertools` — tools for working with sequences
- `functools` — tools for working with functions

---

## 11. Python vs JavaScript — Side-by-Side Concepts

Since you have some JS familiarity, here's a quick mapping of concepts:

| Concept | JavaScript | Python |
|---|---|---|
| Variable declaration | `let x = 5` | `x = 5` |
| Constant | `const PI = 3.14` | `PI = 3.14` (convention only — not enforced) |
| String template | `` `Hello ${name}` `` | `f"Hello {name}"` |
| Array/list | `[1, 2, 3]` | `[1, 2, 3]` |
| Object/dict | `{name: "Craig"}` | `{"name": "Craig"}` |
| `null` check | `if (x === null)` | `if x is None:` |
| Strict equality | `===` | `==` (Python has no `===`, `is` checks identity) |
| Arrow function | `(x) => x * 2` | `lambda x: x * 2` |
| Array `.map()` | `arr.map(fn)` | `[fn(x) for x in arr]` or `map(fn, arr)` |
| Array `.filter()` | `arr.filter(fn)` | `[x for x in arr if fn(x)]` |
| `console.log` | `console.log(x)` | `print(x)` |
| `try/catch` | `try { } catch(e) { }` | `try: ... except Exception as e:` |
| Async function | `async function f() {}` | `async def f():` |
| Await | `await fetch(url)` | `await some_coroutine()` |
| Export/import | `export default` / `import x from 'y'` | `from module import x` |
| `typeof` | `typeof x` | `type(x)` |
| Ternary | `x > 0 ? "pos" : "neg"` | `"pos" if x > 0 else "neg"` |

### The big conceptual differences

**1. Python has list comprehensions — very idiomatic**
```python
# Instead of .map() + .filter()
squares_of_evens = [x**2 for x in range(10) if x % 2 == 0]
# → [0, 4, 16, 36, 64]
```
You'll see this pattern constantly. Learn to read it early.

**2. Python's async model is different**

JavaScript is single-threaded and async by default — the event loop runs constantly. Python's async model (`asyncio`) is opt-in. A normal Python program is synchronous unless you explicitly use `async def` and run an event loop. This is Day 2 of the plan.

**3. Python has no `undefined`**

JS has both `null` (intentional absence) and `undefined` (variable declared but not assigned). Python has only `None`. Simpler.

**4. Python equality: `==` vs `is`**

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b    # True  — same value
a is b    # False — different objects in memory

# Use `is` only for None checks:
if x is None:
    ...
```

**5. Mutability — Python makes it explicit**

```python
# Lists are mutable — you can change them
my_list = [1, 2, 3]
my_list.append(4)   # modifies in place

# Tuples are immutable — you cannot change them
my_tuple = (1, 2, 3)
my_tuple.append(4)  # → AttributeError: 'tuple' object has no attribute 'append'
```

---

## 12. Error Handling

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    print("This always runs")
```

Common exceptions you'll see:
| Exception | When |
|---|---|
| `TypeError` | Wrong type passed to a function |
| `ValueError` | Right type, wrong value |
| `KeyError` | Accessing a dict key that doesn't exist |
| `IndexError` | Accessing a list index out of range |
| `AttributeError` | Calling a method that doesn't exist on an object |
| `ImportError` | Trying to import a module that isn't installed |
| `FileNotFoundError` | Opening a file that doesn't exist |

---

## 13. The Python Ecosystem

### Package manager

**pip** is the default package installer (comes with Python). You'll also use **uv** in this plan — it's a modern, much faster replacement.

```bash
pip install requests         # install a package
pip install -r requirements.txt  # install from a list
uv add requests              # uv equivalent (faster)
```

### Virtual environments

Critical concept: a **virtual environment** is an isolated Python installation for your project. Without it, every package you install goes into a global pool and projects conflict with each other.

```bash
python -m venv .venv        # create a virtual environment
.venv\Scripts\activate      # activate it (Windows)
source .venv/bin/activate   # activate it (Mac/Linux)
```

When active, `pip install` only installs into that project's environment. **Always activate your venv before working.**

`uv` handles this automatically — which is one reason the plan uses it.

### Key libraries in this 30-day plan

| Library | What it does | Day introduced |
|---|---|---|
| **Pydantic** | Data validation — define what shape data must be | Day 1 |
| **asyncio** | Built-in async/concurrent programming | Day 2 |
| **pytest** | Testing framework | Day 5 |
| **FastAPI** | Build REST APIs quickly | Day 8 |
| **SQLAlchemy** | Talk to databases in Python | Day 11 |
| **Redis** | In-memory caching and pub/sub | Day 16 |
| **Celery** | Background job queues | Day 17 |
| **Django** | Full-featured web framework | Day 20 |
| **Docker** | Package your app to run anywhere | Day 25 |

---

## 14. Mental Models to Carry Through All 30 Days

These are the ideas that unify everything you'll learn:

**1. Python is synchronous by default; async is opt-in.**
When you see `async def` and `await`, you're opting into concurrent execution. When you don't, code runs top to bottom, one line at a time.

**2. Types are checked at runtime unless you add tools.**
Python won't stop you from passing a string where a number is expected — Pydantic and mypy are tools that add that safety.

**3. Everything in Python is an object.**
Strings have methods. Functions can be passed around. Classes are objects too. This is why you'll see things like `@decorator` — functions wrapping other functions.

**4. The import system is how everything connects.**
Your code, third-party libraries, and Python's standard library all plug in via `import`. Understanding this makes project structure obvious.

**5. Indentation is structure.**
4 spaces is the convention. Inconsistency causes errors. Set your editor to use spaces, not tabs.

**6. Read error messages top to bottom, but look at the bottom first.**
Python tracebacks show the full call stack. The actual error is at the bottom; the path it took to get there is above. Start reading from the bottom.
