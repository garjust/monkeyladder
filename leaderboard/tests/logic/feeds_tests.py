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
        self.assertEqual(len(self.fixture(ladder=4)), 17)

    def test_get_match_feed_with_user(self):
        matches = self.fixture(user=10)
        self.assertEqual(len(matches), 6)
        for match in matches:
            self.assertEquals(len(MatchPlayer.objects.filter(match=match, user=10)), 1)


class ClimbingLadderFeedTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = feeds.climbing_ladder_feed


class UsersPlayedTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = feeds.users_played

    def test_user_with_no_matches(self):
        self.assertEqual(len(self.fixture(1)), 0)

    def test_invalid_user_returns_empty_list(self):
        self.assertEqual(len(self.fixture(99999)), 0)

    def test_user_with_matches(self):
        users_played = self.fixture(2)
        expected_user_ids = [3, 4, 10]
        for user in users_played:
            if user.id not in expected_user_ids:
                self.fail("User %s should not have been in the list" % user)
            expected_user_ids.remove(user.id)
        if expected_user_ids:
            self.fail("Users were missing from the list: %s" % expected_user_ids)

    def test_invalid_ladder_returns_empty_list(self):
        self.assertEqual(len(self.fixture(2, ladder_id=9999)), 0)

    def test_ladder_with_no_matches(self):
        self.assertEqual(len(self.fixture(2, ladder_id=5)), 0)

    def test_user_and_ladder_with_matches(self):
        users_played = self.fixture(2, ladder_id=4)
        expected_user_ids = [3, 4]
        for user in users_played:
            if user.id not in expected_user_ids:
                self.fail("User %s should not have been in the list" % user)
            expected_user_ids.remove(user.id)
        if expected_user_ids:
            self.fail("Users were missing from the list: %s" % expected_user_ids)
