import unittest

from src.bboard.greeting import greeting


class TestGreeting(unittest.TestCase):
    def test_greeting(self) -> None:
        self.assertEqual(1, len(greeting()))
