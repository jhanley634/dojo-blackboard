import datetime as dt
from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from bboard.models.iss_position import IssPosition
from bboard.models.vehicle_journey import VehicleJourney

engine = create_engine(url="sqlite:////tmp/blackboard.db")


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with sessionmaker(bind=engine)() as sess:
        try:
            yield sess
        finally:
            sess.commit()


def prune_ancient_rows(max_age: dt.timedelta = dt.timedelta(days=1)) -> None:
    """Discard old rows, to prevent the DB file from growing without bound."""
    with get_session() as sess:
        now = dt.datetime.now(dt.timezone.utc)
        sess.query(IssPosition).filter(IssPosition.stamp < now - max_age).delete()
        sess.query(VehicleJourney).filter(VehicleJourney.stamp < now - max_age).delete()
