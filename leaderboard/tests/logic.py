from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Ladder
from leaderboard import logic
from leaderboard.models import Match, MatchPlayer

FIXTURES = ['fixtures/users', 'fixtures/core', 'fixtures/leaderboard']

class GetMatchFeedTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.get_match_feed

    def test_default_size_is_10(self):
        self.assertTrue(Match.objects.filter().count() > 10)
        self.assertEqual(len((self.fixture())), 10)

    def test_get_empty_list_when_no_matches(self):
        self.assertTrue(Match.objects.filter(ladder=2).count() == 0)
        self.assertEqual(len(self.fixture(2)), 0)

    def test_get_match_feed_with_ladder(self):
        self.assertEqual(len(self.fixture(4, size=100)), 17)

class GetPlayersMatchFeedTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.get_players_match_feed

    def test_players_match_feed(self):
        matches = self.fixture(user=10)
        self.assertEqual(len(matches), 6)
        for match in matches:
            self.assertEquals(len(MatchPlayer.objects.filter(match=match, user=10)), 1)

    def test_players_match_feed_with_ladder(self):
        matches = self.fixture(ladder=4, user=10)
        self.assertEqual(len(matches), 5)
        for match in matches:
            self.assertEqual(match.ladder.id, 4)
            self.assertEquals(len(MatchPlayer.objects.filter(match=match, user=10)), 1)

class CountPlayersWinsTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.count_players_wins
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), 4)

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), 0)

class CountPlayersLossesTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.count_players_losses
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), 2)

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), 0)

class CountPlayersMatchesTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.count_players_matches
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), 6)

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), 0)

class CalculatePlayersMatchWinPercentage(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.calculate_players_match_win_percentage
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), 66.66666666666666)

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), 0)

class CountPlayersGamesTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.count_players_games
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), (7, 13))

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), (0, 0))

class CalculatePlayersGameWinPercentage(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.calculate_players_game_win_percentage
        self.has_matches = User.objects.get(pk=10)
        self.no_matches = User.objects.get(pk=1)

    def test_with_player_who_has_played(self):
        self.assertEqual(self.fixture(self.has_matches), 53.84615384615385)

    def test_with_player_with_no_games(self):
        self.assertEqual(self.fixture(self.no_matches), 0)

class GetLadderPlayersTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.get_ladder_players

    def test_get_ladder_players(self):
        players = self.fixture(Ladder.objects.get(pk=3))
        self.assertEqual(type(players), dict)
        self.assertEqual(players['User Longnameduserishappytoprovidetheirlongnametotestnamelength'], User.objects.get(pk=8))
        self.assertEqual(players['user.noname'], User.objects.get(pk=11))
