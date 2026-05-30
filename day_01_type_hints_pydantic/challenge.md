# Day 1 — Challenge: Validated User Model

**Difficulty:** Easy  
**Estimated time:** 45–60 minutes

---

## Goal

Build a Pydantic `User` model with strict validation, then write a function that accepts raw (untrusted) data and either returns a valid model or reports errors clearly.

---

## Requirements

### 1. The `User` model

Create a Pydantic `BaseModel` with these fields:

| Field | Type | Rules |
|---|---|---|
| `id` | `int` | Required, must be positive (> 0) |
| `email` | `EmailStr` | Required, must be a valid email |
| `age` | `int` | Required, must be between 18 and 99 (inclusive) |
| `role` | `Literal["admin", "user"]` | Required, only these two values |
| `username` | `str` | Required, 3–20 chars, no spaces, stored lowercase |
| `bio` | `str \| None` | Optional, defaults to `None`, max 200 chars if provided |

### 2. A field validator on `username`

- Strip leading/trailing whitespace
- Convert to lowercase
- Raise `ValueError` if it contains spaces after stripping
- Raise `ValueError` if length is not between 3 and 20 characters

### 3. A `validate_user(data: dict) -> tuple[User | None, list[dict]]` function

- Accepts a raw dict
- Returns `(user, [])` on success
- Returns `(None, errors)` on failure, where `errors` is the list from `e.errors()`

### 4. Test it manually

At the bottom of your file, call `validate_user` with at least:

- One fully valid input
- One input with a bad email and age too low
- One input with a username containing spaces
- One input with unknown extra fields (hint: configure the model to forbid these)

Print the result of each call clearly.

---

## Expected output (example)

```
[PASS] User(id=1, username='alice', email='alice@example.com', age=25, role='user', bio=None)

[FAIL] 3 error(s):
  - email: value is not a valid email address
  - age: Input should be greater than or equal to 18
  - role: Input should be 'admin' or 'user'

[FAIL] 1 error(s):
  - username: username must not contain spaces

[FAIL] 1 error(s):
  - extra_field: Extra inputs are not permitted
```

---

## Constraints

- Use only `pydantic`, `typing` — no other libraries
- Do not use `try/except` inside the model itself; only in `validate_user`
- The model must be immutable (frozen) — attempts to reassign a field after creation should raise an error

---

## Stretch goals (optional)

1. Add a `@model_validator(mode="after")` that sets `bio` to `f"Hi, I'm {username}."` if `bio` is `None`
2. Write a second function `validate_many(rows: list[dict]) -> tuple[list[User], list[dict]]` that processes a list and separates valid from invalid
3. Add a `display_name` computed field using `@computed_field` that returns `"{username} ({role})"` — look up `computed_field` in the Pydantic v2 docs

---

## File to create

`day_01_type_hints_pydantic/solution.py`

---

## Install dependencies

```bash
pip install pydantic[email]
```
