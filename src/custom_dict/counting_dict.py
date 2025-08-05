from collections import Counter, UserDict
from collections.abc import Generator, Hashable
from copy import deepcopy
from typing import Any, Self


class AccessCounterDict(UserDict[Any, Any]):
    # > Write a class AccessCounterDict that extends dict to count accesses to keys.
    # NB: This class extends a different class, rather than dict.

    def __init__(
        self, initial_data: dict[Hashable, Any] | None = None, /, **kwargs: dict[Any, Any]
    ) -> None:
        d: dict[Hashable, Any] = initial_data or {}
        super().__init__(d, **kwargs)
        self.count: Counter[Hashable] = Counter()  # per-key access counts

    def copy(self) -> "AccessCounterDict":
        c = AccessCounterDict()
        c.update(self)
        c.reset_counts()
        return c

    def __deepcopy__(self, _memo: dict[int, Any]) -> "AccessCounterDict":
        c = AccessCounterDict()
        c.count = deepcopy(self.count)
        for k, v in self.items():
            c[k] = deepcopy(v)
        return c

    def reset_counts(self) -> Self:
        self.count.clear()
        return self

    def get_count(self, key: Hashable) -> int:
        return self.count[key]

    def __delitem__(self, key: Hashable) -> None:
        del self.count[key]
        return super().__delitem__(key)

    def __getitem__(self, key: Hashable) -> Any:
        self.count[key] += 1
        return super().__getitem__(key)

    def unread_keys(self) -> Generator[Hashable]:
        """Generates keys that were stored, are still valid, and have not been read."""
        return (k for k in self if self.count[k] == 0)
