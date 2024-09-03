import unittest

from src.bboard.demo.clock_display import clock_display, clock_reading


class ClockDisplayTest(unittest.TestCase):
    def test_clock_display(self) -> None:
        self.assertGreaterEqual(len(clock_display()), 587)
        self.assertGreaterEqual(len(clock_reading()), 39)
