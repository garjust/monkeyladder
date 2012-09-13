from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Ladder
from leaderboard.logic import rankings

FIXTURES = ['fixtures/users', 'fixtures/core', 'fixtures/leaderboard']

class GetLadderPlayersTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = rankings.get_ladder_players

    def test_get_ladder_players(self):
        players = self.fixture(Ladder.objects.get(pk=3))
        self.assertEqual(type(players), dict)
        self.assertEqual(players['User Longnameduserishappytoprovidetheirlongnametotestnamelength'], User.objects.get(pk=8))
        self.assertEqual(players['user.noname'], User.objects.get(pk=11))

