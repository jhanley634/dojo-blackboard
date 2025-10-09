from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utc import UtcDateTime

from bboard.models.iss_position import Base

if TYPE_CHECKING:
    import datetime as dt


class VehicleJourney(Base):  # type: ignore [misc]
    __tablename__ = "vehicle_journey"
    stamp: Mapped[dt.datetime] = mapped_column(UtcDateTime(), primary_key=True)
    agency: Mapped[str] = mapped_column(primary_key=True)
    vehicle_ref: Mapped[str] = mapped_column(primary_key=True)
    latitude: Mapped[float]
    longitude: Mapped[float]
