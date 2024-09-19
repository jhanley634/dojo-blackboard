import datetime as dt
from typing import Any

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_utc import UtcDateTime


class Base(DeclarativeBase):
    def _asdict(self) -> dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class IssPosition(Base):
    __tablename__ = "iss_position"
    stamp: Mapped[dt.datetime] = mapped_column(UtcDateTime(), primary_key=True)
    latitude: Mapped[float]
    longitude: Mapped[float]

    def __repr__(self) -> str:
        return f"IssPosition(stamp='{self.stamp}', latitude={self.latitude!r}, longitude={self.longitude!r})"
