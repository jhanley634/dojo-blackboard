from collections.abc import Callable
from functools import wraps
from time import time
from typing import Any


def timed(func: Callable[..., list[int]]) -> Callable[..., list[int]]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> list[int]:
        t0 = time()
        result = func(*args, **kwargs)
        elapsed = time() - t0
        if elapsed > 0.9:  # Don't bother commenting on a "short" run.
            print(f"\nFunction '{func.__name__}' took {elapsed:.6f} seconds.")
        return result

    return wrapper
