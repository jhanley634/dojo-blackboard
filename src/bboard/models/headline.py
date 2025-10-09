from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utc import UtcDateTime

from bboard.models.iss_position import Base

if TYPE_CHECKING:
    import datetime as dt


class Headline(Base):  # type: ignore [misc]
    __tablename__ = "headline"
    hash: Mapped[str] = mapped_column(primary_key=True)
    stamp: Mapped[dt.datetime] = mapped_column(UtcDateTime(), index=True)
    url: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)


class Article(Base):  # type: ignore [misc]
    __tablename__ = "article"
    hash: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str]
