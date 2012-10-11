from django.contrib.auth.models import User
from django.test import TestCase

from leaderboard.logic import stats

FIXTURES = ['fixtures/users', 'fixtures/core', 'fixtures/leaderboard']

class CountPlayersWinsTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = stats.count_players_wins
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), 4)

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), 0)

class CountPlayersLossesTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = stats.count_players_losses
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), 2)

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), 0)

class CountPlayersMatchesTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = stats.count_players_matches
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), 6)

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), 0)

class CalculatePlayersMatchWinPercentage(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = stats.calculate_players_match_win_percentage
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), 66.66666666666666)

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), 0)

class CountPlayersGamesTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = stats.count_players_games
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), (7, 13))

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), (0, 0))

class CalculatePlayersGameWinPercentage(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = stats.calculate_players_game_win_percentage
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), 53.84615384615385)

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), 0)
