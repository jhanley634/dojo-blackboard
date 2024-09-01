import datetime as dt

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_utc import UtcDateTime


class Base(DeclarativeBase):
    pass


class IssPosition(Base):
    __tablename__ = "iss_position"
    stamp: Mapped[dt.datetime] = mapped_column(UtcDateTime(), primary_key=True)
    latitude: Mapped[float]
    longitude: Mapped[float]

    def __repr__(self) -> str:
        return f"IssPosition(stamp='{self.stamp}', latitude={self.latitude!r}, longitude={self.longitude!r})"
