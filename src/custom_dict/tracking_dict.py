from collections import UserDict
from collections.abc import Generator, Hashable
from copy import deepcopy
from typing import Any


class TrackingDict(UserDict[Any, Any]):
    """
    A dict that tracks whether the app ever bothered to read what it stored.

    This can help with finding things like overly verbose DB queries,
    application reporting function bugs, and API mismatches.
    Call the `.unread_keys()` generator to find entries that have not yet been read.

    Space complexity:
        We store twice as many key pointers as `dict`.
        And possibly twice as many key bytes, though not in
        certain caching cases, such as when keys are small ints.
    Time complexity:
        Scanning `.unread_keys()` incurs linear O(N) cost to scan `.keys()`.
        No change for any other operations, though note that OO dispatch via
        `UserDict` is more expensive than calling into the `dict` native C code.
    """

    def __init__(
        self, initial_data: dict[Hashable, Any] | None = None, /, **kwargs: dict[Any, Any]
    ) -> None:
        d: dict[Hashable, Any] = initial_data or {}
        super().__init__(d, **kwargs)
        self.used: set[Hashable] = set()  # keys the app has read / consumed

    def copy(self) -> "TrackingDict":
        c = TrackingDict()
        c.update(self)
        return c

    def __deepcopy__(self, _memo: dict[int, Any]) -> "TrackingDict":
        c = TrackingDict()
        c.used = deepcopy(self.used)
        for k, v in self.items():
            c[k] = deepcopy(v)
        return c

    def __delitem__(self, key: Hashable) -> None:
        self.used.discard(key)
        return super().__delitem__(key)

    def __getitem__(self, key: Hashable) -> Any:
        self.used.add(key)
        return super().__getitem__(key)

    def unread_keys(self) -> Generator[Hashable]:
        """Generates keys that were stored, are still valid, and have not been read."""
        for k in self.keys():
            if k not in self.used:
                yield k
