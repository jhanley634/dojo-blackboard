from collections import Counter, UserDict
from typing import Any


class AccessCounterDict(UserDict[Any, Any]):
    # > Write a class AccessCounterDict that extends dict to count accesses to keys.
    # NB: This class extends a different class, rather than dict.

    def __init__(
        self, initial_data: dict[Any, Any] | None = None, /, **kwargs: dict[Any, Any]
    ) -> None:
        d: dict[Any, Any] = initial_data or {}
        super().__init__(d, **kwargs)
        self.count: Counter[Any] = Counter()  # per-key access counts
