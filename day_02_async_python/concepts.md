# Day 2 — Async Python

---

## Concept Anchor

A single-threaded event loop handles concurrency by pausing tasks that are waiting on I/O (network, disk) and switching to other ready tasks — no extra threads needed.

This is the key distinction between:
- **Concurrency** — doing many things by interleaving them (async, one thread)
- **Parallelism** — doing many things simultaneously on multiple CPU cores

Web servers are I/O-bound — most time is spent waiting for responses, not computing — which makes async a natural fit.

---

## 1. `async` / `await` — The Basics

An `async def` function is a **coroutine** — it doesn't run immediately when called. You must `await` it (or schedule it) to actually execute it.

```python
import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)   # yields control back to the event loop for 1s
    print("World")

asyncio.run(say_hello())    # entry point — creates the event loop and runs it
```

`await` can only be used **inside** an `async def` function. Using `time.sleep()` inside async code is a bug — it blocks the entire event loop and defeats the purpose.

| Blocking (wrong in async) | Non-blocking (correct) |
|---|---|
| `time.sleep(1)` | `await asyncio.sleep(1)` |
| `requests.get(url)` | `await aiohttp.ClientSession().get(url)` |
| `open(file).read()` | `await aiofiles.open(file).read()` |

---

## 2. `asyncio.gather` — Run Coroutines Concurrently

`asyncio.gather` takes multiple coroutines and runs them concurrently. It waits for **all** of them to finish and returns their results in the same order as the inputs.

```python
import asyncio

async def fetch(url: str) -> str:
    await asyncio.sleep(1)
    return f"Response from {url}"

async def main():
    results = await asyncio.gather(
        fetch("https://api.example.com/a"),
        fetch("https://api.example.com/b"),
        fetch("https://api.example.com/c"),
    )
    print(results)  # ['Response from .../a', '.../b', '.../c']

asyncio.run(main())
# Total time: ~1s (not 3s) — all three run concurrently
```

You can also unpack a list into `gather` using `*`:

```python
coroutines = [fetch(url) for url in urls]
results = await asyncio.gather(*coroutines)
```

---

## 3. `asyncio.create_task` — Fire and Don't Immediately Wait

`create_task` schedules a coroutine to run on the event loop **without** waiting for it right away. This lets you start tasks, do other work, then collect results later.

```python
async def main():
    task_a = asyncio.create_task(fetch("https://api.example.com/a"))
    task_b = asyncio.create_task(fetch("https://api.example.com/b"))

    # Both tasks are now running concurrently in the background
    # You can do other work here...

    result_a = await task_a   # now wait for each
    result_b = await task_b
```

`gather` is more convenient when you want all results at once. `create_task` is useful when you need finer control — e.g., cancelling individual tasks, or starting tasks at different times.

---

## 4. The Event Loop

The event loop is the scheduler at the heart of asyncio. It keeps a queue of coroutines and callbacks, runs the next ready one, and switches away whenever a coroutine hits an `await`.

```
Event Loop
│
├── Task A running  →  hits await  →  paused
├── Task B running  →  hits await  →  paused
├── Task A resumes (I/O ready)  →  completes
└── Task B resumes (I/O ready)  →  completes
```

You rarely interact with the event loop directly. `asyncio.run(main())` creates one, runs your top-level coroutine, then closes it.

---

## 5. `asyncio.Queue` — Producer / Consumer

`asyncio.Queue` is an async-safe queue for passing work between coroutines. A producer puts items in; workers take items out.

```python
import asyncio

async def producer(queue: asyncio.Queue):
    for i in range(5):
        await queue.put(i)
        print(f"Produced {i}")
    await queue.put(None)    # sentinel to signal workers to stop

async def worker(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), worker(queue))

asyncio.run(main())
```

This pattern is useful when you want to limit how many items are in flight at once — `asyncio.Queue(maxsize=N)` blocks the producer when the queue is full.

---

## 6. `asyncio.wait_for` — Timeouts

Wrap a coroutine with `asyncio.wait_for` to cancel it if it takes too long.

```python
async def slow_fetch(url: str) -> str:
    await asyncio.sleep(5)
    return f"Response from {url}"

async def main():
    try:
        result = await asyncio.wait_for(slow_fetch("https://example.com"), timeout=2.0)
    except asyncio.TimeoutError:
        print("Request timed out")

asyncio.run(main())
```

---

## Summary

| Concept | One-liner |
|---|---|
| `async def` | Defines a coroutine — must be awaited to run |
| `await` | Yields control to the event loop until the awaited thing completes |
| `asyncio.run()` | Entry point — creates the event loop and runs a coroutine |
| `asyncio.gather()` | Run multiple coroutines concurrently, collect all results |
| `asyncio.create_task()` | Schedule a coroutine without immediately waiting for it |
| `asyncio.sleep()` | Non-blocking sleep — yields control to the event loop |
| `asyncio.Queue` | Async-safe queue for producer/consumer patterns |
| `asyncio.wait_for()` | Wrap a coroutine with a timeout |
