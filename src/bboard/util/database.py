from contextlib import contextmanager
from typing import TYPE_CHECKING

from pint import Quantity
from pint import UnitRegistry as Unit
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from bboard.models.iss_position import IssPosition
from bboard.models.vehicle_journey import VehicleJourney

if TYPE_CHECKING:
    from collections.abc import Generator

engine: Engine = create_engine(url="sqlite:////tmp/blackboard.db")


@contextmanager
def get_session() -> Generator[Session]:
    with sessionmaker(bind=engine)() as sess:
        try:
            yield sess
        finally:
            sess.commit()


_one_day = 1 * Unit().day
assert isinstance(_one_day, Quantity)

MINUTES_PER_DAY = _one_day.to("minutes").magnitude
assert MINUTES_PER_DAY == 1440


def prune_ancient_rows(limit: int = MINUTES_PER_DAY) -> None:
    """Discard yesterday's rows, to prevent the DB file from growing without bound."""
    vj = VehicleJourney
    with get_session() as sess:
        stamps = (
            sess.query(vj.stamp).order_by(vj.stamp.desc()).group_by(vj.stamp).limit(limit).all()
        )
        if len(stamps) > 0:
            (ancient,) = stamps[-1]
            sess.query(vj).filter(vj.stamp < ancient).delete()
            sess.query(IssPosition).filter(IssPosition.stamp < ancient).delete()

            count = sess.query(vj).group_by(vj.stamp).count()
            assert count <= limit, count
