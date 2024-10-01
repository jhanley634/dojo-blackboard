import datetime as dt

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utc import UtcDateTime

from bboard.models.iss_position import Base


class Article(Base):  # type: ignore [misc]
    __tablename__ = "article"
    hash: Mapped[str] = mapped_column(primary_key=True)
    stamp: Mapped[dt.datetime] = mapped_column(UtcDateTime(), index=True)
    source: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)
    publisher_link: Mapped[str]
    source_icon: Mapped[str]
    og: Mapped[str]
