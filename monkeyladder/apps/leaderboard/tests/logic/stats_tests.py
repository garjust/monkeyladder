from django.test import TestCase

from leaderboard.logic import stats

FIXTURES = ['fixtures/users', 'fixtures/ladders', 'fixtures/leaderboard']


class GetMatchStatsTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = stats.get_match_stats

    def test_all_match_stats(self):
        self.assertEqual(self.fixture(2), (3, 6))
        self.assertEqual(self.fixture(1), (0, 0))

    def test_ladder_specific_match_stats(self):
        self.assertEqual(self.fixture(2, ladder=5), (0, 0))
        self.assertEqual(self.fixture(2, ladder=4), (2, 3))
        self.assertEqual(self.fixture(1, ladder=4), (0, 0))

    def test_user_specific_match_stats(self):
        self.assertEqual(self.fixture(2, other_user_id=3), (3, 4))
        self.assertEqual(self.fixture(1, other_user_id=2), (0, 0))

    def test_user_and_ladder_specific_match_stats(self):
        self.assertEqual(self.fixture(2, ladder=4, other_user_id=3), (2, 2))
        self.assertEqual(self.fixture(2, ladder=5, other_user_id=3), (0, 0))


class GetGameStatsTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = stats.get_game_stats

    def test_all_game_stats(self):
        self.assertEqual(self.fixture(2), (7, 14))
        self.assertEqual(self.fixture(1), (0, 0))

    def test_ladder_specific_game_stats(self):
        self.assertEqual(self.fixture(2, ladder=5), (0, 0))
        self.assertEqual(self.fixture(2, ladder=4), (4, 6))
        self.assertEqual(self.fixture(1, ladder=4), (0, 0))

    def test_user_specific_game_stats(self):
        self.assertEqual(self.fixture(2, other_user_id=3), (7, 10))
        self.assertEqual(self.fixture(2, other_user_id=1), (0, 0))

    def test_user_and_ladder_specific_game_stats(self):
        self.assertEqual(self.fixture(2, ladder=4, other_user_id=3), (4, 4))
        self.assertEqual(self.fixture(2, ladder=5, other_user_id=3), (0, 0))
