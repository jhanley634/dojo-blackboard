import datetime as dt
import unittest
from datetime import timezone as tz

from sqlalchemy import Engine, Table, create_engine

from bboard.models.iss_position import Base, IssPosition
from bboard.transit.iss import _get_iss_breadcrumbs, iss_lng_lat, iss_world_map
from bboard.util.credentials import repo_top, throw
from bboard.util.database import engine, get_session
from bboard.util.fs import temp_dir
from bboard.util.testing import _do_nothing, mark_slow_integration_test

Base.metadata.create_all(engine)


def _truncate_to_one_minute(seconds: int) -> int:
    s = seconds // 60 * 60
    hmsz = f"{dt.datetime.fromtimestamp(s,tz.utc)}".split()[1]
    assert hmsz.endswith(":00+00:00")
    return s


def _create_tz_temp_db(db_file: str = "tz_test.sqlite") -> Engine:
    filespec = temp_dir() / db_file
    filespec.unlink(missing_ok=True)
    eng = create_engine(f"sqlite:///{filespec}")
    Base.metadata.create_all(eng)
    return eng


class IssTest(unittest.TestCase):
    def test_repo_top(self) -> None:
        self.assertTrue(f"{repo_top}".endswith("dojo-blackboard"))
        self.assertTrue((repo_top / "src/bboard").is_dir())

    def test_iss_lng_lat(self) -> None:
        iss_lng_lat()

    @mark_slow_integration_test  # type: ignore [misc]
    def test_iss_world_map(self) -> None:
        limit = 6
        self.assertGreater(len(list(_get_iss_breadcrumbs(limit))), 0)
        self.assertTrue(iss_world_map(limit).exists())

    def test_no_op(self) -> None:
        _do_nothing(self)

    def test_asdict(self) -> None:
        with get_session() as sess:
            row = sess.query(IssPosition).order_by(IssPosition.stamp.desc()).limit(1).one_or_none()
            assert row, 'Please "make run" before running this test.'
            self.assertEqual(
                "stamp, latitude, longitude",
                ", ".join(row._asdict().keys()),
            )

    def test_timezone_roundtrip(self) -> None:
        """Verifies that a timestamp can be stored and retrieved, keeping its UTC timezone.

        The PostgreSQL driver gets this right, but by default MySQL and SQLite do not,
        so our model uses the sqlalchemy_utc package to fix it.
        """
        august = 1725124921
        fromtimestamp = dt.datetime.fromtimestamp

        stamp1 = fromtimestamp(august, tz.utc)
        seconds = _truncate_to_one_minute(int(stamp1.timestamp()))
        self.assertEqual("2024-08-31 17:22:01+00:00", f"{stamp1}")
        self.assertEqual("2024-08-31 17:22:01+00:00", stamp1.isoformat(" "))
        self.assertEqual("2024-08-31_17:22:01+00:00", stamp1.isoformat("_"))
        self.assertEqual("2024-08-31T17:22:01+00:00", stamp1.isoformat())
        self.assertEqual("2024-08-31T17:22:00+00:00", fromtimestamp(seconds, tz.utc).isoformat())
        self.assertEqual(tz.utc, stamp1.tzinfo)
        self.assertEqual("UTC", stamp1.tzname())

        eng = _create_tz_temp_db()
        pos = IssPosition(stamp=stamp1, latitude=0.0, longitude=0.0)
        tbl = IssPosition.__table__
        assert isinstance(tbl, Table)
        expected = (
            "(datetime.datetime(2024, 8, 31, 17, 22, 1, tzinfo=datetime.timezone.utc), 0.0, 0.0)"
        )
        with eng.connect() as conn:
            conn.execute(tbl.insert(), [pos.__dict__])
            result = conn.execute(tbl.select())
            row = result.first() or throw(ValueError("no rows"))
            self.assertEqual(expected, f"{row}")
            self.assertEqual(stamp1, row.stamp)  # thanks to sqlalchemy_utc on non-PG DBs
