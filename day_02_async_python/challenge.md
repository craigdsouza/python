# Day 2 — Challenge: Async Fetch Simulator

**Difficulty:** Easy  
**Estimated time:** 45–60 minutes

---

## Goal

Write an async program that simulates fetching multiple URLs concurrently, and compare it against a sequential version to see why async matters.

---

## Requirements

### 1. A `fetch(url: str) -> str` coroutine

- Simulates a network delay using `asyncio.sleep` with a **random duration between 0.1 and 0.5 seconds**
- Returns a string like `"Response from {url}"` after the delay

### 2. A `fetch_all(urls: list[str]) -> list[str]` coroutine

- Fetches all URLs **concurrently** using `asyncio.gather`
- Returns the list of result strings

### 3. A `fetch_sequential(urls: list[str]) -> list[str]` coroutine

- Fetches each URL **one at a time** (no concurrency)
- Returns the list of result strings

### 4. Time both and print a comparison

In `if __name__ == "__main__"`, run both functions on the same list of 5+ URLs and print:
- Each result as it completes
- Total elapsed time for each approach

---

## Expected output (example)

```
=== Concurrent ===
Response from https://api.example.com/users
Response from https://api.example.com/posts
Response from https://api.example.com/photos
Response from https://api.example.com/comments
Response from https://api.example.com/todos
Concurrent time: 0.48s

=== Sequential ===
Response from https://api.example.com/users
Response from https://api.example.com/posts
Response from https://api.example.com/photos
Response from https://api.example.com/comments
Response from https://api.example.com/todos
Sequential time: 1.73s
```

(Exact times will vary since delays are random.)

---

## Constraints

- Use only the standard library (`asyncio`, `random`, `time`)
- Do not use `time.sleep` anywhere — only `asyncio.sleep`
- No external packages needed

---

## Stretch Goals (optional)

1. Rewrite `fetch_all` using `asyncio.create_task` instead of `asyncio.gather`
2. Add an `asyncio.Queue`-based version: a producer enqueues URLs, and N worker coroutines consume and fetch them concurrently
3. Add a per-request timeout using `asyncio.wait_for` — if a fetch exceeds 0.4s, record `"TIMEOUT: {url}"` instead of a response

---

## File to edit

`day_02_async_python/solution.py`
