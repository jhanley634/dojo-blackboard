from collections import UserDict
from collections.abc import Generator
from typing import Any


class TrackingDict(UserDict[Any, Any]):
    def __init__(
        self, initial_data: dict[Any, Any] | None = None, /, **kwargs: dict[str, Any]
    ) -> None:
        d: dict[Any, Any] = initial_data or {}
        super().__init__(d, **kwargs)
        self.used: set[str] = set()  # Keys the app has read / consumed

    def copy(self) -> "TrackingDict":
        c = TrackingDict()
        c.update(self)
        return c

    def __delitem__(self, key: Any) -> None:
        self.used.discard(key)
        return super().__delitem__(key)

    def __getitem__(self, key: Any) -> Any:
        self.used.add(key)
        return super().__getitem__(key)

    def unread_keys(self) -> Generator[str]:
        for k in self.keys():
            if k not in self.used:
                yield k
