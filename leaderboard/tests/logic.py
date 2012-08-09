from django.test import TestCase

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

    def test_match_feed_with_ladder(self):
        matches = self.fixture(ladder=4)
        self.assertEqual(len(matches), 10)
        for match in matches:
            self.assertEqual(match.ladder.id, 4)

    def test_match_feed_with_user(self):
        matches = self.fixture(user=10)
        self.assertEqual(len(matches), 5)
        for match in matches:
            self.assertEquals(len(MatchPlayer.objects.filter(match=match, user=10)), 1)

    def test_match_feed_with_ladder_and_user(self):
        matches = self.fixture(ladder=4, user=10)
        self.assertEqual(len(matches), 5)
        for match in matches:
            self.assertEqual(match.ladder.id, 4)
            self.assertEquals(len(MatchPlayer.objects.filter(match=match, user=10)), 1)
