from django.test import TestCase

from leaderboard import logic

FIXTURES = ['fixtures/users', 'fixtures/core', 'fixtures/leaderboard']

class GetMatchFeedTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixutre = logic.get_match_feed

    def test_feed_should_have_ladders_matches(self):
        raise Exception("FAIL")

