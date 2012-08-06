from django.test import TestCase

from leaderboard import logic

FIXTURES = ['fixtures/users', 'fixtures/core', 'fixtures/leaderboard']

class AdjustRankingsTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.adjust_rankings

    def test_simple_swap(self):
        self.assertEqual(1 + 1, 2)
        raise AssertionError()

