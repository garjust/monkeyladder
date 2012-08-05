from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from core import logic
from core.models import Ladder, Watcher

FIXTURES = ['fixtures/users', 'fixtures/core']

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