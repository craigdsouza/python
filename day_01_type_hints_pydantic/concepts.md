# Day 1 — Type Hints & Pydantic

---

## 1. Type Hints (`typing` module)

Type hints tell readers (and tools like `mypy`) what types a variable or function expects. They are not enforced at runtime by Python itself.

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

age: int = 25
scores: list[int] = [90, 85, 78]
lookup: dict[str, int] = {"alice": 1}
```

### Common types from `typing`

| Type | Use |
|---|---|
| `Optional[X]` | `X` or `None` — same as `X \| None` in Python 3.10+ |
| `Union[X, Y]` | Either X or Y |
| `Literal["a", "b"]` | Only these exact values |
| `Any` | Opt out of type checking |
| `TypeVar` | Generic placeholder for a type |
| `Callable[[int], str]` | A function taking int, returning str |
| `ClassVar[X]` | Class-level variable, not instance |

```python
from typing import Optional, Union, Literal

def find_user(id: int) -> Optional[str]:   # returns str or None
    ...

def parse(val: Union[str, int]) -> str:    # str or int accepted
    return str(val)

def set_role(role: Literal["admin", "user"]) -> None:
    ...
```

### Python 3.10+ shorthand

```python
def find(id: int) -> str | None: ...      # same as Optional[str]
def parse(val: str | int) -> str: ...     # same as Union[str, int]
```

---

## 2. `Annotated` — Attaching Metadata to Types

`Annotated[T, metadata]` lets you attach extra information to a type. Pydantic uses this to add validation constraints without subclassing.

```python
from typing import Annotated
from pydantic import Field

# The type is still `int`, but Pydantic reads the Field metadata
Age = Annotated[int, Field(ge=18, le=99)]

class User(BaseModel):
    age: Age
```

This is cleaner than repeating `Field(ge=18, le=99)` everywhere — you define it once as a type alias.

---

## 3. Pydantic v2 — Core Concepts

Pydantic validates data at instantiation time. If data is invalid, it raises a `ValidationError` with detailed messages.

### Basic model

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class User(BaseModel):
    id: int
    email: EmailStr            # validates email format
    age: int = Field(ge=18, le=99)  # 18 <= age <= 99
    role: Literal["admin", "user"]
    nickname: str | None = None     # optional, defaults to None
```

### Creating instances

```python
# From keyword args
u = User(id=1, email="alice@example.com", age=25, role="user")

# From a dict (useful when data comes from JSON/API)
data = {"id": 1, "email": "alice@example.com", "age": 25, "role": "user"}
u = User(**data)

# From JSON string
u = User.model_validate_json('{"id":1,"email":"a@b.com","age":25,"role":"user"}')
```

### Serialising models back out

```python
u.model_dump()                        # → plain dict
u.model_dump(exclude={"id"})          # exclude fields
u.model_dump(include={"email","role"})
u.model_dump_json()                   # → JSON string
```

---

## 4. Field Validators

### `field_validator` — validate a single field

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def username_no_spaces(cls, v: str) -> str:
        if " " in v:
            raise ValueError("username must not contain spaces")
        return v.lower()   # you can also transform the value
```

### `model_validator` — validate across multiple fields

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def check_order(self) -> "DateRange":
        if self.end <= self.start:
            raise ValueError("end must be greater than start")
        return self
```

`mode="after"` runs after all individual fields are validated.
`mode="before"` runs on the raw input dict before field parsing.

---

## 5. Handling `ValidationError`

```python
from pydantic import ValidationError

try:
    u = User(id="not-an-int", email="bad", age=5, role="superuser")
except ValidationError as e:
    print(e)            # human-readable summary
    print(e.errors())   # list of dicts, one per error
    # Each error dict has: loc, msg, type, input
```

Example `e.errors()` output:
```python
[
  {"loc": ("id",),    "msg": "Input should be a valid integer", "type": "int_parsing"},
  {"loc": ("email",), "msg": "value is not a valid email address", "type": "value_error"},
  {"loc": ("age",),   "msg": "Input should be greater than or equal to 18", "type": "greater_than_equal"},
  {"loc": ("role",),  "msg": "Input should be 'admin' or 'user'", "type": "literal_error"},
]
```

---

## 6. `model_config` — Model-Level Settings

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,   # strip leading/trailing spaces from strings
        frozen=True,                 # make instances immutable (hashable)
        extra="forbid",              # raise error if extra fields are passed
    )

    name: str
    age: int
```

`extra="forbid"` is useful for APIs where unknown fields should be rejected.

---

## 7. Key `mypy` / IDE Benefits

Type hints power static analysis tools:
- **mypy** catches type errors before runtime: `mypy my_file.py`
- **ruff** lints code style and common mistakes
- IDEs (VS Code, PyCharm) use hints for autocomplete and inline error highlighting

```bash
pip install mypy pydantic[email]
mypy day1.py
```

---

## Summary

| Concept | One-liner |
|---|---|
| Type hints | Annotations for readability and tooling — not runtime enforced |
| `Annotated` | Attach metadata (e.g. constraints) to a type |
| `Pydantic BaseModel` | Validates data on construction, raises `ValidationError` |
| `Field()` | Add constraints (`ge`, `le`, `min_length`, etc.) to a field |
| `field_validator` | Custom per-field validation logic |
| `model_validator` | Cross-field validation after all fields are set |
| `model_dump()` | Serialize model back to a plain dict |
| `model_config` | Model-level settings (immutability, extra fields, etc.) |
