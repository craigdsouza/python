import functools
import time
from contextlib import contextmanager

# Challenge: Build a @retry decorator and a timer() context manager, then compose them.
#
# See challenge.md for full requirements.


# --- Part 1: @retry decorator ---
# A parametrized decorator: retry(times, delay, exceptions) → decorator → wrapper
# - Retry only on exceptions listed in `exceptions`
# - Wait `delay` seconds between attempts
# - Re-raise the last exception if all attempts fail

def retry(times: int = 3, delay: float = 0.5, exceptions: tuple = (Exception,)):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            # TODO: loop `times` times
            # TODO: call fn(*args, **kwargs) inside a try/except
            # TODO: on failure, check if the exception is in `exceptions`
            #       - if yes: print attempt message, sleep, continue
            #       - if no: re-raise immediately (no retry)
            # TODO: after all attempts, re-raise the last exception
            pass
        return wrapper
    return decorator


# --- Part 2: timer() context manager ---
# Use @contextmanager from contextlib.
# Record start time before yield, print elapsed time in finally.

@contextmanager
def timer(label: str = ""):
    # TODO: record start time
    # TODO: yield (execution passes to the with block here)
    # TODO: in a finally block, compute and print elapsed time
    yield


# --- Part 3: flaky_mock function ---
# Raises ValueError for the first `fail_times` calls, then returns "success".
# Decorate it with @retry so the retries happen automatically.

@retry(times=3, delay=0.1, exceptions=(ValueError,))
def flaky_mock(fail_times: int = 2) -> str:
    # TODO: use a mutable container to track call count across calls
    # Hint: a list works — e.g. counter = [0], then counter[0] += 1
    # Or use a global counter variable.
    # Raise ValueError for the first fail_times calls, then return "success"
    pass


# --- Part 4: main block ---
# Compose retry + timer, test wrong-exception propagation, test exhausted retries.

if __name__ == "__main__":
    print("=== Test 1: flaky_mock with retry + timer ===")
    # TODO: run flaky_mock() inside a `with timer("flaky_mock"):` block
    # TODO: print the result


    print("\n=== Test 2: wrong exception type — no retry ===")
    # TODO: define (or decorate inline) a function that raises TypeError
    # TODO: show it propagates immediately without retrying


    print("\n=== Test 3: all retries exhausted ===")
    # TODO: define a function that always raises ValueError("always fails")
    # TODO: decorate with @retry(times=3, delay=0.05, exceptions=(ValueError,))
    # TODO: call it inside try/except and print the error message
