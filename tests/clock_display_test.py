import unittest

from bboard.demo.clock_display import clock_display, clock_reading, stop_watch


class ClockDisplayTest(unittest.TestCase):
    def test_clock_display(self) -> None:
        self.assertGreaterEqual(len(clock_display()), 587)
        self.assertGreaterEqual(len(clock_reading()), 39)

    def test_stop_watch(self) -> None:
        self.assertGreaterEqual(len(stop_watch()), 1350)
