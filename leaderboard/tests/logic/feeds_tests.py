from django.test import TestCase

from leaderboard.logic import feeds
from leaderboard.models import MatchPlayer

FIXTURES = ['fixtures/users', 'fixtures/core', 'fixtures/leaderboard']


class GetMatchFeedTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = feeds.get_match_feed

    def test_get_empty_list_when_no_matches(self):
        self.assertEqual(len(self.fixture(ladder=2)), 0)

    def test_get_match_feed_with_ladder(self):
        self.assertEqual(len(self.fixture(ladder=4, size=100)), 17)

    def test_get_match_feed_with_user(self):
        matches = self.fixture(user=10)
        self.assertEqual(len(matches), 6)
        for match in matches:
            self.assertEquals(len(MatchPlayer.objects.filter(match=match, user=10)), 1)
