from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from core import logic
from core.models import Ladder, Watcher, LadderConfigurationKey

FIXTURES = ['fixtures/users', 'fixtures/core']

class IntOr404Test(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.int_or_404

    def test_valid_int(self):
        self.assertEqual(self.fixture("23"), 23)

    def test_raise_404_if_int_invalid(self):
        with self.assertRaises(Http404):
            self.fixture("sd")

class GetLadderOr404Test(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.get_ladder_or_404

    def test_get_ladder(self):
        self.assertEqual(self.fixture(pk=1), Ladder.objects.get(pk=1))

    def test_raise_404_if_ladder_dne(self):
        self.assertRaises(Http404, self.fixture, pk=99999)

class PublicLadderFeedTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.public_ladder_feed
        self.user = User.objects.get(pk=1)

    def test_feed_should_have_public_ladders(self):
        ladders = self.fixture()
        for ladder in Ladder.objects.filter(is_private=False):
            self.assertIn(ladder, ladders)

    def test_feed_should_not_have_private_ladders(self):
        ladders = self.fixture()
        for ladder in Ladder.objects.filter(is_private=True):
            self.assertNotIn(ladder, ladders)

    def test_feed_should_not_have_watched_ladders_if_user(self):
        ladders = self.fixture(user=self.user)
        for ladder in map(lambda w: w.ladder, self.user.watcher_set.all()):
            self.assertNotIn(ladder, ladders)

    def test_change_size_of_feed(self):
        self.assertEqual(len(self.fixture(size=0)), 0)

class WatchedLadderFeedTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.watched_ladder_feed
        self.user = User.objects.get(pk=1)

    def test_feed_should_have_watched_ladders(self):
        feed = self.fixture(self.user)
        watchers = Watcher.objects.filter(user=self.user)
        for watcher in watchers:
            self.assertIn(watcher.ladder, feed)

    def test_change_size_of_feed(self):
        self.assertEqual(len(self.fixture(self.user, size=0)), 0)

class LadderWatchersTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.ladder_watchers

    def test_get_correct_watchers(self):
        ladder = Ladder.objects.get(pk=1)
        watchers = self.fixture(ladder)
        for watcher in Watcher.objects.filter(ladder=ladder):
            self.assertIn(watcher, watchers)

class GetConfigTest(TestCase):
    fixtures = FIXTURES + ['fixtures/leaderboard']

    def setUp(self):
        self.fixture = logic.get_config

    def test_key_with_unconfigured_ladder(self):
        self.assertEqual(self.fixture(4, 'leaderboard.auto_take_first'), True)

    def test_single_key_returns_single_value(self):
        self.assertEqual(self.fixture(3, 'leaderboard.auto_take_first'), False)

    def test_bad_key_raises_exception(self):
        with self.assertRaises(LadderConfigurationKey.DoesNotExist):
            self.fixture(3, 'leaderboard.swap_Range')

    def test_multiple_keys_returns_dictionary(self):
        self.assertEqual(self.fixture(3, 'leaderboard.auto_take_first', 'leaderboard.swap_range'), {
            'leaderboard.auto_take_first': False, 'leaderboard.swap_range': 0,
        })
