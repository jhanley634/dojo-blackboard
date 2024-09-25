from collections.abc import Callable
from os import getenv
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., None])


def mark_slow_integration_test(test_func: Any) -> Any:
    """
    Marks a "slow" test that we may wish to skip.

    The decorated TestCase function won't be run
    when we set environment variable SKIP_SLOW=1.
    """
    func: Any = _do_nothing
    should_skip = getenv("SKIP_SLOW", "0") == "1"
    if not should_skip:
        func = test_func
    return func


def _do_nothing(self: Any) -> None:
    pass
