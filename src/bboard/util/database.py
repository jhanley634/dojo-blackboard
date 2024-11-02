from collections.abc import Generator
from contextlib import contextmanager

from pint import Quantity
from pint import UnitRegistry as Unit
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from bboard.models.iss_position import IssPosition
from bboard.models.vehicle_journey import VehicleJourney

engine: Engine = create_engine(url="sqlite:////tmp/blackboard.db")


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with sessionmaker(bind=engine)() as sess:
        try:
            yield sess
        finally:
            sess.commit()


_one_day: Quantity = 1 * Unit().day
MINUTES_PER_DAY = _one_day.to("minutes").magnitude
assert MINUTES_PER_DAY == 1440.0


def prune_ancient_rows(limit: int = MINUTES_PER_DAY) -> None:
    """Discard yesterday's rows, to prevent the DB file from growing without bound."""
    VJ = VehicleJourney
    with get_session() as sess:
        stamps = (
            sess.query(VJ.stamp).order_by(VJ.stamp.desc()).group_by(VJ.stamp).limit(limit).all()
        )
        if len(stamps) > 0:
            (ancient,) = stamps[-1]
            sess.query(VJ).filter(VJ.stamp < ancient).delete()
            sess.query(IssPosition).filter(IssPosition.stamp < ancient).delete()

            count = sess.query(VJ).group_by(VJ.stamp).count()
            assert count <= limit, count
